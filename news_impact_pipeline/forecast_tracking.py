#!/usr/bin/env python3
"""
forecast_tracking.py

Feedback-loop della pipeline: verifica a posteriori le "previsioni" implicite
nelle schede (`daily_analysis/AAAA-MM-GG/news_NN.md`) contro il rendimento
realizzato letto dal DB di mercato.

COSA CONTA COME "PREVISIONE"
----------------------------
Ogni scheda contiene, per ciascun asset e finestra (T+1/3/5/10), la statistica
event-study degli episodi storici analoghi: mediana, p25, p75, N. Da qui
estraiamo due segnali falsificabili:
  - DISTRIBUZIONE (faro): la banda storica [p25, p75] (il 50% centrale). Se la
    metodologia e' ben calibrata, ~50% dei realizzati deve caderci dentro.
  - DIREZIONE (secondaria): il segno della mediana storica. Confrontato col
    segno del rendimento realizzato (hit/miss). Le previsioni "piatte"
    (|mediana| < FLAT_THRESHOLD) sono marcate no-call ed escluse dall'hit-rate
    (la scheda non si e' sbilanciata su una direzione), ma restano valide per
    la copertura.

ARCHITETTURA
------------
Un unico artefatto append-only: `daily_analysis/forecast_ledger.csv`. Una riga
per (scheda × asset × orizzonte):
  - colonne "made"  scritte al momento del backfill/scrittura scheda;
  - colonne "eval"  riempite quando la previsione e' MATURA (il DB ha abbastanza
    giorni di borsa dopo l'ancora) — riusa event_study.compute_returns.

Sottocomandi:
  backfill   scansiona le schede e accoda al ledger le previsioni non ancora presenti
  evaluate   riempie le righe mature con realizzato / in_iqr / hit_dir / abs_error
  scorecard  aggrega le metriche e scrive daily_analysis/_scorecard/AAAA-Www.md
  run        backfill + evaluate + scorecard (usato dal job settimanale)

Convenzioni metodologiche: identiche a event_study.py (anchor = primo trading
day >= data; T+N = N-esimo trading day dopo l'anchor; prezzo = COALESCE(adj_close,
close)). Il realizzato di una previsione fatta il giorno D usa D come evento:
misura cosa e' successo DOPO che la chiamata e' stata fatta (no look-ahead).
"""

import argparse
import csv
import math
import re
import sqlite3
import subprocess
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import markdown

from bootstrap_market_data import DB_PATH
from event_study import compute_returns
from render_report import CSS, MD_EXTENSIONS
from analogues import _norm_theme


# --- Percorsi --------------------------------------------------------------
DAILY_DIR     = Path.home() / "Claude" / "mercati_finanza" / "daily_analysis"
LEDGER_PATH   = DAILY_DIR / "forecast_ledger.csv"
SCORECARD_DIR = DAILY_DIR / "_scorecard"

# Soglia "piatto": sotto questa |mediana| (in %) la scheda non si sbilancia su
# una direzione → esclusa dall'hit-rate direzionale, inclusa nella copertura.
FLAT_THRESHOLD = 0.10

# Sotto questo N le metriche sono "indicative only" (coerente con CLAUDE.md).
SAMPLE_SIZE_WARNING_THRESHOLD = 20

# N minimo di previsioni mature perché un ASSET compaia nella tabella per-ticker
# (sotto questa soglia l'IC per-asset è troppo rumoroso per dire qualcosa).
ASSET_MIN_N = 50

# N minimo per includere un asset nel calcolo dell'IC per-asset (soglia più bassa
# di ASSET_MIN_N: qui non mostriamo il singolo asset, lo aggreghiamo — serve solo
# che il suo IC non sia puro rumore. Usata anche per-orizzonte, dove gli N si
# dividono per 4).
IC_ASSET_MIN_N = 15

# Cartella-giorno valida = nome strettamente AAAA-MM-GG (esclude _scorecard,
# *_manual_backup, ecc.).
DAY_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

FIELDS = [
    "made_date", "slug", "card_path", "asset", "horizon",
    "expected_median", "expected_mean", "hist_p25", "hist_p75",
    "n_analogues", "sentiment", "confidence", "directional",
    # colonne riempite in evaluate:
    "anchor_date", "realized_return", "in_iqr", "hit_dir", "abs_error", "eval_date",
]

KEY = ("made_date", "slug", "asset", "horizon")


# --- Parsing delle schede --------------------------------------------------

def _parse_pct(cell: str):
    """'+0.18%' / '-2.30%' / 'n/a' / '**6**' → float o None."""
    if cell is None:
        return None
    c = cell.strip().strip("*").strip()
    c = c.replace("%", "").replace("+", "").strip()
    if not c or c.lower() == "n/a":
        return None
    try:
        return float(c)
    except ValueError:
        return None


def _table_row_cells(line: str) -> list[str]:
    """Spezza una riga di tabella markdown nelle sue celle (senza i bordi)."""
    parts = [p.strip() for p in line.strip().strip("|").split("|")]
    return parts


def parse_card(path: Path) -> list[dict]:
    """
    Estrae le previsioni (made-side) da una scheda. Una entry per
    (asset × orizzonte). Lista vuota se la scheda non ha tabelle event-study.
    """
    text = path.read_text(encoding="utf-8")

    m = re.search(r"\*\*Data analisi\*\*:\s*(\d{4}-\d{2}-\d{2})", text)
    made_date = m.group(1) if m else path.parent.name
    m = re.search(r"\*\*Slug\*\*:\s*([^\n<]+)", text)
    slug = m.group(1).strip() if m else path.stem

    def _classif(field):
        mm = re.search(rf"\|\s*`{field}`\s*\|\s*([^\|<\n]+)", text)
        return mm.group(1).strip() if mm else ""
    sentiment  = _classif("sentiment")
    confidence = _classif("confidence")

    rel_path = str(path.relative_to(DAILY_DIR))
    entries = []

    # Ogni blocco event-study inizia con "### Event study — `TICKER`" e arriva
    # fino al prossimo heading "### " (o fine file).
    blocks = re.split(r"\n###\s+", text)
    for blk in blocks:
        mt = re.match(r"Event study\s+—\s+`([^`]+)`", blk.strip())
        if not mt:
            continue
        ticker = mt.group(1).strip()

        lines = blk.splitlines()
        # header con gli orizzonti
        horizons = None
        rows = {}
        for ln in lines:
            if horizons is None and re.search(r"\bStat\b", ln) and "T+" in ln:
                horizons = [int(h) for h in re.findall(r"T\+(\d+)", ln)]
                continue
            if horizons is None:
                continue
            cells = _table_row_cells(ln)
            if not cells:
                continue
            label = cells[0].strip().strip("*").lower()
            if label in ("media", "mediana", "p25", "p75") or label == "n":
                vals = [_parse_pct(c) for c in cells[1:1 + len(horizons)]]
                rows[label] = vals

        if horizons is None or "mediana" not in rows:
            continue

        for i, hz in enumerate(horizons):
            median = rows.get("mediana", [None] * len(horizons))[i]
            if median is None:
                continue
            p25  = rows.get("p25",  [None] * len(horizons))[i]
            p75  = rows.get("p75",  [None] * len(horizons))[i]
            mean = rows.get("media", [None] * len(horizons))[i]
            nval = rows.get("n",     [None] * len(horizons))[i]
            entries.append({
                "made_date": made_date,
                "slug": slug,
                "card_path": rel_path,
                "asset": ticker,
                "horizon": hz,
                "expected_median": median,
                "expected_mean": mean,
                "hist_p25": p25,
                "hist_p75": p75,
                "n_analogues": int(nval) if nval is not None else "",
                "sentiment": sentiment,
                "confidence": confidence,
                "directional": 1 if abs(median) >= FLAT_THRESHOLD else 0,
            })
    return entries


def discover_cards() -> list[Path]:
    cards = []
    if not DAILY_DIR.exists():
        return cards
    for day_dir in sorted(DAILY_DIR.iterdir()):
        if not day_dir.is_dir() or not DAY_DIR_RE.match(day_dir.name):
            continue
        cards.extend(sorted(day_dir.glob("news_*.md")))
    return cards


# --- Ledger I/O ------------------------------------------------------------

def load_ledger() -> list[dict]:
    if not LEDGER_PATH.exists():
        return []
    with LEDGER_PATH.open(newline="", encoding="utf-8") as fp:
        return list(csv.DictReader(fp))


def write_ledger(rows: list[dict]) -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    def sort_key(r):
        return (r["made_date"], r["slug"], r["asset"], int(r["horizon"]))
    rows = sorted(rows, key=sort_key)
    with LEDGER_PATH.open("w", newline="", encoding="utf-8") as fp:
        w = csv.DictWriter(fp, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def _key(r: dict) -> tuple:
    return (str(r["made_date"]), str(r["slug"]), str(r["asset"]), str(r["horizon"]))


# --- Sottocomandi ----------------------------------------------------------

def cmd_backfill() -> None:
    existing = load_ledger()
    seen = {_key(r) for r in existing}
    added = 0
    for card in discover_cards():
        for e in parse_card(card):
            for k in FIELDS:
                e.setdefault(k, "")
            if _key(e) not in seen:
                existing.append(e)
                seen.add(_key(e))
                added += 1
    write_ledger(existing)
    print(f"[backfill] schede scansionate, righe nel ledger: {len(existing)} "
          f"(+{added} nuove). File: {LEDGER_PATH}")


def cmd_evaluate() -> None:
    rows = load_ledger()
    if not rows:
        print("[evaluate] ledger vuoto — esegui prima 'backfill'.")
        return

    # Raggruppa per (asset, made_date) le righe non ancora valutate.
    pending = [r for r in rows if not r.get("realized_return")]
    if not pending:
        print("[evaluate] nessuna previsione in attesa di valutazione.")
        return

    today = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    filled = 0
    try:
        # cache per (asset, made_date) → compute_returns
        cache: dict[tuple, dict] = {}
        for r in pending:
            asset = r["asset"]
            md = r["made_date"]
            hz = int(r["horizon"])
            ckey = (asset, md)
            if ckey not in cache:
                try:
                    ed = date.fromisoformat(md)
                except ValueError:
                    cache[ckey] = None
                    continue
                try:
                    res = compute_returns(conn, asset, [ed], [1, 3, 5, 10])
                except ValueError:
                    cache[ckey] = None
                    continue
                cache[ckey] = res["per_event"][0] if res["per_event"] else None
            pe = cache[ckey]
            if pe is None:
                continue
            realized = pe["returns"].get(hz)
            if realized is None:
                continue  # orizzonte non ancora maturo nel DB
            p25 = float(r["hist_p25"]) if r.get("hist_p25") not in ("", None) else None
            p75 = float(r["hist_p75"]) if r.get("hist_p75") not in ("", None) else None
            med = float(r["expected_median"]) if r.get("expected_median") not in ("", None) else None

            r["anchor_date"] = pe["anchor_date"].isoformat()
            r["realized_return"] = f"{realized:.4f}"
            if p25 is not None and p75 is not None:
                lo, hi = min(p25, p75), max(p25, p75)
                r["in_iqr"] = 1 if lo <= realized <= hi else 0
            if med is not None and abs(med) >= FLAT_THRESHOLD:
                r["hit_dir"] = 1 if (realized > 0) == (med > 0) else 0
            else:
                r["hit_dir"] = ""  # no-call
            if med is not None:
                r["abs_error"] = f"{abs(realized - med):.4f}"
            r["eval_date"] = today
            filled += 1
    finally:
        conn.close()

    write_ledger(rows)
    matured = sum(1 for r in rows if r.get("realized_return"))
    print(f"[evaluate] valutate ora: {filled}. Totale mature: {matured}/{len(rows)}.")


# --- Metriche --------------------------------------------------------------

def _wilson_ci(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (None, None)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def _spearman(xs: list[float], ys: list[float]):
    # Spearman = Pearson sui ranghi (evita la dipendenza da scipy che pandas
    # richiederebbe con method="spearman").
    if len(xs) < 3:
        return None
    rx = pd.Series(xs).rank()
    ry = pd.Series(ys).rank()
    s = rx.corr(ry, method="pearson")
    return None if pd.isna(s) else float(s)


def _ic_within_assets(rows: list[dict], min_n: int = IC_ASSET_MIN_N):
    """IC calcolato DENTRO ciascun asset, poi media pesata per numerosità.

    Perché non basta lo Spearman su tutte le righe insieme (versione precedente):
    mettere nello stesso ranking ^VIX (che si muove del 3%) ed EURUSD=X (0,15%),
    e insieme T+1 con T+10, fa sì che la correlazione catturi in buona parte le
    differenze di SCALA fra asset invece dell'abilità predittiva. Misurato sul
    ledger al 2026-08-10: pooled +0.072 contro **+0.024** per-asset → il pooled
    sovrastimava di ~3x. Qui confrontiamo ogni previsione solo con altre previsioni
    sullo STESSO asset, che è la domanda vera ("quando la storia si sbilancia di
    più su questo asset, il movimento reale è davvero maggiore?").

    Restituisce (ic_pesato, n_righe_usate, n_asset_usati) — (None, 0, 0) se nessun
    asset raggiunge min_n.
    """
    by_asset: dict = {}
    for r in rows:
        if r.get("_med") is not None:
            by_asset.setdefault(r["asset"], []).append(r)
    num = den = 0.0
    n_assets = 0
    for sub in by_asset.values():
        if len(sub) < min_n:
            continue
        ic = _spearman([r["_med"] for r in sub], [r["_real"] for r in sub])
        if ic is None:
            continue
        num += ic * len(sub)
        den += len(sub)
        n_assets += 1
    return (num / den if den else None), int(den), n_assets


def _pct(x):
    return "n/a" if x is None else f"{x * 100:.0f}%"


def _verdict(kind: str, value):
    """Semaforo ✅/⚠️/❌ per una metrica. `value` e' una frazione 0–1 (copertura,
    hit-rate) o la correlazione di rango (ic). None → trattino."""
    if value is None:
        return "—"
    if kind == "coverage":          # ideale ~50%: basso = intervalli stretti, alto = larghi
        if 0.40 <= value <= 0.70:
            return "✅"
        if 0.25 <= value < 0.40 or 0.70 < value <= 0.85:
            return "⚠️"
        return "❌"
    if kind == "hit":               # baseline monetina = 50%
        if value >= 0.60:
            return "✅"
        if value >= 0.45:
            return "⚠️"
        return "❌"
    if kind == "ic":                # correlazione di rango atteso vs realizzato
        if value >= 0.20:
            return "✅"
        if value >= 0.0:
            return "⚠️"
        return "❌"
    return "—"


def _volte_su_10(frac):
    """0.73 → '7 volte su 10'. Per rendere le percentuali leggibili a colpo d'occhio."""
    return "n/a" if frac is None else f"{round(frac * 10)} volte su 10"


_THEME_CACHE: dict = {}

def _theme_of_card(rel_path: str) -> str:
    """Estrae `primary_theme` dalla scheda (path relativo a DAILY_DIR), con cache.
    Il ledger non memorizza il tema → lo rileggiamo dalla scheda referenziata."""
    if rel_path in _THEME_CACHE:
        return _THEME_CACHE[rel_path]
    theme = ""
    try:
        text = (DAILY_DIR / rel_path).read_text(encoding="utf-8")
        m = re.search(r"\|\s*`primary_theme`\s*\|\s*([^\|<\n]+)", text)
        if m:
            # Normalizza come in analogues.py: alcune schede annotano il tema tra
            # parentesi ('monetary_policy (sub: china / pboc)') — senza normalizzare
            # diventa un tema-fantasma distinto nella tabella per-tema della
            # scorecard (visto in W32: "structural_themes (AI/semis)", N=9 isolato
            # dal vero structural_themes, N=201). Stesso fix, stesso bug, file diverso.
            theme = _norm_theme(m.group(1))
    except Exception:
        pass
    _THEME_CACHE[rel_path] = theme
    return theme


def _write_scorecard_html(md_text: str, md_path: Path, label: str) -> Path:
    """
    Rende la scorecard markdown in un HTML impaginato, nello stesso stile dei
    report giornalieri (CSS condiviso da render_report). Output accanto al .md.
    """
    body = markdown.markdown(md_text, extensions=MD_EXTENSIONS)
    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Scorecard previsioni — {label}</title>
<style>{CSS}</style>
</head>
<body>
  <header class="report-head">
    <div class="date-label">News-to-Market Impact · Feedback loop</div>
    <h1>🎯 Scorecard previsioni — {label}</h1>
    <p class="subtitle">Verifica a posteriori delle previsioni delle schede contro il realizzato di mercato. Faro = copertura distribuzionale [p25,p75] (ideale ~50%). Statistiche descrittive, non segnali operativi.</p>
  </header>
  <section class="doc">
{body}
  </section>
  <footer>
    Generato da News-to-Market Impact Pipeline · feedback loop settimanale · le metriche con N&lt;20 sono "indicative only".
  </footer>
</body>
</html>
"""
    out = md_path.with_suffix(".html")
    out.write_text(html, encoding="utf-8")
    return out


def cmd_scorecard(open_browser: bool = False) -> None:
    rows = [r for r in load_ledger() if r.get("realized_return")]
    SCORECARD_DIR.mkdir(parents=True, exist_ok=True)
    iso_year, iso_week, _ = date.today().isocalendar()
    out_path = SCORECARD_DIR / f"{iso_year}-W{iso_week:02d}.md"

    L = []
    L.append(f"# Scorecard previsioni — {iso_year}-W{iso_week:02d}\n")
    L.append(f"_Generata: {datetime.now().isoformat(timespec='seconds')}_\n")

    if not rows:
        L.append("Nessuna previsione ancora matura. Riprova quando il DB avra' "
                 "abbastanza giorni di borsa dopo le schede.\n")
        text = "\n".join(L)
        out_path.write_text(text, encoding="utf-8")
        html_path = _write_scorecard_html(text, out_path, f"{iso_year}-W{iso_week:02d}")
        print(f"[scorecard] nessuna previsione matura. Scritti stub: {out_path} + {html_path.name}")
        if open_browser:
            subprocess.run(["open", str(html_path)], check=False)
        return

    # Tipizza
    for r in rows:
        r["_hz"] = int(r["horizon"])
        r["_real"] = float(r["realized_return"])
        r["_med"] = float(r["expected_median"]) if r["expected_median"] not in ("", None) else None
        r["_iqr"] = int(r["in_iqr"]) if r.get("in_iqr") not in ("", None) else None
        r["_hit"] = int(r["hit_dir"]) if r.get("hit_dir") not in ("", None) else None

    horizons = sorted({r["_hz"] for r in rows})
    n_total = len(rows)
    n_cards = len({(r["made_date"], r["slug"]) for r in rows})
    L.append(f"**Previsioni mature**: {n_total} (da {n_cards} schede) — "
             f"orizzonti {', '.join('T+'+str(h) for h in horizons)}.\n")
    if n_total < SAMPLE_SIZE_WARNING_THRESHOLD:
        L.append(f"> ⚠ **INDICATIVE ONLY** — N={n_total} < "
                 f"{SAMPLE_SIZE_WARNING_THRESHOLD}. Questa scorecard costruisce un "
                 f"track record; non e' ancora un verdetto sulla metodologia.\n")

    # --- Metriche complessive (riusate sia in "In sintesi" che nelle tabelle) ---
    cov_all = [r for r in rows if r["_iqr"] is not None]
    overall_cov = (sum(r["_iqr"] for r in cov_all) / len(cov_all)) if cov_all else None
    hit_all = [r for r in rows if r["_hit"] is not None]
    overall_hit = (sum(r["_hit"] for r in hit_all) / len(hit_all)) if hit_all else None
    med_all = [r for r in rows if r["_med"] is not None]
    # IC "onesto": calcolato dentro ogni asset e poi mediato (vedi _ic_within_assets).
    # Il pooled resta calcolato solo per il confronto trasparente nella sezione 3.
    overall_ic, _, _ = _ic_within_assets(med_all)
    overall_ic_pooled = _spearman([r["_med"] for r in med_all], [r["_real"] for r in med_all])

    # 0) IN SINTESI — lettura in parole povere, auto-generata dai numeri sopra.
    L.append("## In sintesi\n")
    L.append(f"Su **{n_total} previsioni** ormai verificabili, il sistema:\n")
    if overall_hit is not None:
        L.append(f"- ha **azzeccato la direzione {_volte_su_10(overall_hit)}** "
                 f"({_pct(overall_hit)} dei casi) — tirare una monetina darebbe 50% "
                 f"{_verdict('hit', overall_hit)}")
    if overall_cov is not None:
        taratura = ("un filo larghi" if overall_cov > 0.55
                    else "un filo stretti" if overall_cov < 0.45 else "ben tarati")
        L.append(f"- i suoi **intervalli storici hanno contenuto il risultato reale "
                 f"{_volte_su_10(overall_cov)}** ({_pct(overall_cov)}; l'ideale è ~50% "
                 f"→ gli intervalli sono {taratura}) {_verdict('coverage', overall_cov)}")
    if overall_ic is not None:
        senso = ("ciò che la storia suggeriva tende ad avverarsi" if overall_ic >= 0.10
                 else "in aggregato lo storico non anticipa il realizzato"
                 if overall_ic > -0.05
                 else "in aggregato lo storico punta nella direzione sbagliata")
        L.append(f"- correlazione di rango **{overall_ic:+.2f}** tra atteso e "
                 f"realizzato, misurata a parità di asset: {senso} "
                 f"{_verdict('ic', overall_ic)}")
        L.append(f"  <br>⚠️ Non leggerlo come «mediocri ovunque»: è la media di due "
                 f"gruppi opposti che si annullano — alcuni ticker hanno un vantaggio "
                 f"reale, altri sono sistematicamente rovesciati. La **sezione 5-bis** "
                 f"dice quali sono.")
    L.append("")
    L.append("> Legenda semaforo: ✅ buono · ⚠️ da monitorare · ❌ scarso. "
             "Le tabelle sotto spaccano gli stessi numeri per orizzonte temporale.\n")

    # 1) COPERTURA (faro): % di realizzati dentro [p25, p75]; ideale ~50%.
    L.append("## 1. Quanto spesso il risultato è caduto nella banda storica "
             "_(copertura; banda p25–p75)_\n")
    L.append("**Come si legge:** ogni scheda dà un intervallo storico (il 50% centrale "
             "degli episodi analoghi). Se è ben tarato, ~**50%** dei risultati reali ci "
             "cade dentro. Molto sopra = intervalli troppo larghi (poco utili); molto "
             "sotto = troppo stretti (sovra-sicuri).\n")
    L.append("| Orizzonte | Copertura | N | Esito |")
    L.append("|---|---|---|---|")
    for h in horizons + ["overall"]:
        sub = [r for r in rows if (h == "overall" or r["_hz"] == h) and r["_iqr"] is not None]
        if not sub:
            continue
        cov = sum(r["_iqr"] for r in sub) / len(sub)
        label = "**overall**" if h == "overall" else f"T+{h}"
        L.append(f"| {label} | {_pct(cov)} | {len(sub)} | {_verdict('coverage', cov)} |")
    L.append("")
    # Flag automatico: orizzonti con bande troppo strette (copertura << 50%).
    narrow = []
    for h in horizons:
        sub = [r for r in rows if r["_hz"] == h and r["_iqr"] is not None]
        if sub and (sum(r["_iqr"] for r in sub) / len(sub)) < 0.35:
            narrow.append(f"T+{h}")
    if narrow:
        L.append(f"> ⚠️ **Ampiezza inaffidabile a {', '.join(narrow)}**: la copertura è "
                 "ben sotto il 50%, cioè gli intervalli storici sono troppo stretti e i "
                 "movimenti reali ne escono spesso. A questi orizzonti **fidati della "
                 "direzione, non dell'ampiezza** della banda (la dispersione vera è "
                 "maggiore di quella stimata dagli analoghi).\n")

    # 2) DIREZIONE (secondaria): hit-rate sul segno della mediana; baseline 50%.
    L.append("## 2. Quanto spesso ha azzeccato la direzione _(hit-rate: su/giù)_\n")
    L.append("**Come si legge:** la scheda dice se l'asset, storicamente, tendeva a "
             "salire o scendere. Qui contiamo quante volte il segno reale ha coinciso. "
             f"Tirare una monetina darebbe **50%**. Escluse le previsioni 'piatte' "
             f"(|mediana| < {FLAT_THRESHOLD}%: la scheda non si è sbilanciata). "
             "L'IC 95% è il margine di incertezza statistica (Wilson).\n")
    L.append("| Orizzonte | Hit-rate | N | margine 95% | Esito |")
    L.append("|---|---|---|---|---|")
    for h in horizons + ["overall"]:
        sub = [r for r in rows if (h == "overall" or r["_hz"] == h) and r["_hit"] is not None]
        if not sub:
            continue
        k = sum(r["_hit"] for r in sub)
        hit = k / len(sub)
        lo, hi = _wilson_ci(k, len(sub))
        label = "**overall**" if h == "overall" else f"T+{h}"
        L.append(f"| {label} | {_pct(hit)} | {len(sub)} | {_pct(lo)}–{_pct(hi)} | "
                 f"{_verdict('hit', hit)} |")
    L.append("")

    # 3) Information Coefficient (Spearman mediana attesa vs realizzato)
    L.append("## 3. C'è correlazione tra atteso e realizzato? "
             "_(Information Coefficient, Spearman)_\n")
    L.append("**Come si legge:** misura se, **a parità di asset**, le previsioni più "
             "sbilanciate corrispondono davvero a movimenti reali più grandi "
             "(correlazione di rango, da −1 a +1). **>0** = lo storico ha contenuto "
             "informativo; **~0** = nessun legame; **<0** = controproducente.\n")
    L.append("La colonna **IC (per-asset)** è quella da guardare: confronta ogni "
             "previsione solo con altre sullo stesso ticker. La colonna *IC (pooled)* "
             "è il vecchio calcolo che mescolava tutti gli asset insieme — la teniamo "
             "per trasparenza, ma **sovrastima**, perché gran parte della correlazione "
             "veniva dal fatto ovvio che asset volatili (^VIX) hanno numeri più grandi "
             "di asset tranquilli (EURUSD=X), non da capacità predittiva.\n")
    L.append("| Orizzonte | IC (per-asset) | N | Esito | _IC (pooled)_ |")
    L.append("|---|---|---|---|---|")
    for h in horizons + ["overall"]:
        sub = [r for r in rows if (h == "overall" or r["_hz"] == h) and r["_med"] is not None]
        ic_w, n_used, _ = _ic_within_assets(sub)
        ic_pool = _spearman([r["_med"] for r in sub], [r["_real"] for r in sub])
        label = "**overall**" if h == "overall" else f"T+{h}"
        ic_s = "n/a" if ic_w is None else f"{ic_w:+.2f}"
        pool_s = "n/a" if ic_pool is None else f"_{ic_pool:+.2f}_"
        L.append(f"| {label} | {ic_s} | {n_used} | {_verdict('ic', ic_w)} | {pool_s} |")
    L.append("")

    # 4) Stratificazione per confidence
    L.append("## 4. Le previsioni 'sicure' vanno davvero meglio? _(per confidence)_\n")
    L.append("**Come si legge:** il classificatore si auto-assegna una confidence "
             "(high/medium/low). Se è onesto con sé stesso, le 'high' dovrebbero avere "
             "copertura e hit-rate migliori delle 'low'.\n")
    L.append("| Confidence | Copertura | Hit-rate | N |")
    L.append("|---|---|---|---|")
    for conf in ["high", "medium", "low"]:
        sub = [r for r in rows if (r.get("confidence") or "").lower() == conf]
        if not sub:
            continue
        cov_sub = [r for r in sub if r["_iqr"] is not None]
        hit_sub = [r for r in sub if r["_hit"] is not None]
        cov = (sum(r["_iqr"] for r in cov_sub) / len(cov_sub)) if cov_sub else None
        hit = (sum(r["_hit"] for r in hit_sub) / len(hit_sub)) if hit_sub else None
        L.append(f"| {conf} | {_pct(cov)} | {_pct(hit)} | {len(sub)} |")
    L.append("")

    # 5) Stratificazione per TEMA (primary_theme della scheda, riletto dal file)
    L.append("## 5. Quali temi prevediamo meglio? _(per primary_theme)_\n")
    L.append("**Come si legge:** raggruppa le previsioni per tema della notizia "
             "(politica monetaria, energia/commodity, dati macro, ecc.). Rivela **dove "
             "il sistema ha un vantaggio e dove no**: un tema con hit-rate alto e IC "
             "positivo è terreno solido; uno vicino al 50% / IC≈0 va trattato con "
             "cautela. Ordinato per numerosità (N).\n")
    L.append("| Tema | Copertura | Hit-rate | IC | N |")
    L.append("|---|---|---|---|---|")
    by_theme: dict = {}
    for r in rows:
        by_theme.setdefault(_theme_of_card(r["card_path"]) or "(non determinato)", []).append(r)
    for theme, sub in sorted(by_theme.items(), key=lambda kv: -len(kv[1])):
        cov_sub = [r for r in sub if r["_iqr"] is not None]
        hit_sub = [r for r in sub if r["_hit"] is not None]
        med_sub = [r for r in sub if r["_med"] is not None]
        cov = (sum(r["_iqr"] for r in cov_sub) / len(cov_sub)) if cov_sub else None
        hit = (sum(r["_hit"] for r in hit_sub) / len(hit_sub)) if hit_sub else None
        ic = _spearman([r["_med"] for r in med_sub], [r["_real"] for r in med_sub])
        ic_s = "n/a" if ic is None else f"{ic:+.2f}"
        L.append(f"| {theme} | {_pct(cov)} | {_pct(hit)} | {ic_s} | {len(sub)} |")
    L.append("")

    # 5-bis) Stratificazione per ASSET.
    # Aggiunta 2026-08-10 dopo un audit: era il punto cieco della scorecard. L'IC
    # aggregato (~+0.07) nasconde una spaccatura netta e STABILE nel tempo: forte
    # sugli asset di rischio (^VIX +0.27, EEM/^NDX/^STOXX50E ~+0.16), ma
    # sistematicamente NEGATIVO su rifugio/tassi/dollaro (IEF -0.33, DX-Y.NYB
    # -0.12 con hit-rate 31% = 3.4 sigma sotto il caso, GC=F -0.09). Senza questa
    # tabella il difetto è rimasto invisibile per mesi.
    L.append("## 5-bis. Su quali ASSET prevediamo meglio? _(per ticker)_\n")
    L.append("**Come si legge:** è la vista più operativa. Un IC negativo con N "
             "grande NON è rumore: significa che su quell'asset la lettura storica "
             "è **sistematicamente rovesciata**, e conviene non usarla (o invertirla "
             "consapevolmente). Solo asset con almeno "
             f"{ASSET_MIN_N} previsioni mature. Ordinato per numerosità.\n")
    L.append("| Asset | Copertura | Hit-rate | IC | N | Giudizio |")
    L.append("|---|---|---|---|---|---|")
    by_asset: dict = {}
    for r in rows:
        by_asset.setdefault(r["asset"], []).append(r)
    for asset, sub in sorted(by_asset.items(), key=lambda kv: -len(kv[1])):
        if len(sub) < ASSET_MIN_N:
            continue
        cov_sub = [r for r in sub if r["_iqr"] is not None]
        hit_sub = [r for r in sub if r["_hit"] is not None]
        med_sub = [r for r in sub if r["_med"] is not None]
        cov = (sum(r["_iqr"] for r in cov_sub) / len(cov_sub)) if cov_sub else None
        hit = (sum(r["_hit"] for r in hit_sub) / len(hit_sub)) if hit_sub else None
        ic = _spearman([r["_med"] for r in med_sub], [r["_real"] for r in med_sub])
        if ic is None:
            verdict = "n/d"
        elif ic <= -0.05:
            verdict = "❌ controproducente"
        elif ic >= 0.10:
            verdict = "✅ affidabile"
        else:
            verdict = "⚠️ debole"
        ic_s = "n/a" if ic is None else f"{ic:+.2f}"
        L.append(f"| {asset} | {_pct(cov)} | {_pct(hit)} | {ic_s} | {len(sub)} | {verdict} |")
    L.append("")
    bad = [a for a, s in by_asset.items() if len(s) >= ASSET_MIN_N
           and (_spearman([r["_med"] for r in s if r["_med"] is not None],
                          [r["_real"] for r in s if r["_med"] is not None]) or 0) <= -0.05]
    if bad:
        L.append(f"> ❌ **Asset da NON usare per la direzione**: {', '.join(sorted(bad))}. "
                 "Su questi la mediana storica ha correlazione negativa col realizzato: "
                 "riportare pure l'event study, ma **non trarne una direzione attesa** "
                 "(o dichiarare esplicitamente che il segno storico è inaffidabile).\n")

    # 6) Magnitudine (de-enfatizzata: le schede disconoscono la trasferibilita')
    L.append("## 6. Errore tipico di grandezza _(MAE)_ — secondario\n")
    L.append("**Come si legge:** di quanto, in media, il movimento reale si è "
             "discostato dalla mediana storica (in punti percentuali). ⚠ Le schede "
             "stesse avvertono che la *grandezza* storica non è trasferibile: tienilo "
             "come riferimento, non come metrica di qualità.\n")
    L.append("| Orizzonte | MAE | N |")
    L.append("|---|---|---|")
    for h in horizons + ["overall"]:
        sub = [r for r in rows if (h == "overall" or r["_hz"] == h)
               and r.get("abs_error") not in ("", None)]
        if not sub:
            continue
        mae = sum(float(r["abs_error"]) for r in sub) / len(sub)
        label = "**overall**" if h == "overall" else f"T+{h}"
        L.append(f"| {label} | {mae:.2f}% | {len(sub)} |")
    L.append("")

    # Glossario (termini tecnici in parole povere)
    L.append("## Glossario\n")
    L.append("- **Previsione matura**: scheda per cui il DB ha ormai abbastanza giorni "
             "di borsa dopo la notizia per misurare cosa è successo.")
    L.append("- **Orizzonte T+N**: N giorni di borsa dopo l'evento (T+1 = giorno dopo).")
    L.append("- **Banda p25–p75**: l'intervallo che racchiude il 50% centrale degli "
             "episodi storici analoghi; il resto (25% sotto, 25% sopra) è la coda.")
    L.append("- **Mediana storica**: il movimento 'tipico' (valore centrale) degli "
             "episodi analoghi; ne usiamo il *segno* per la direzione.")
    L.append("- **No-call**: previsione troppo piatta per dire su/giù "
             f"(|mediana| < {FLAT_THRESHOLD}%) → conta per la copertura, non per l'hit-rate.")
    L.append("- **Hit-rate**: % di volte in cui la direzione prevista era giusta.")
    L.append("- **IC (Information Coefficient)**: correlazione di rango tra atteso e "
             "realizzato (Spearman); >0 = lo storico informa.")
    L.append("- **IC per-asset vs pooled**: il *per-asset* confronta ogni previsione "
             "solo con altre sullo stesso ticker, poi fa la media — è la misura "
             "onesta dell'abilità. Il *pooled* mette tutti gli asset in un'unica "
             "classifica e perciò premia il fatto ovvio che ^VIX si muove più di "
             "EURUSD=X: gonfia il risultato (al 2026-08-10: +0.07 pooled contro "
             "+0.02 reale). Usiamo il per-asset come numero ufficiale.")
    L.append("- **Margine 95% (Wilson)**: con così pochi dati il vero hit-rate sta "
             "verosimilmente in questo intervallo, non esattamente sul numero mostrato.\n")

    # Caveat fissi
    L.append("## Caveat\n")
    L.append("- **N piccolo**: poche schede/giorno × pochi asset. Le metriche si "
             "stabilizzano solo su orizzonte di mesi.")
    L.append("- **Finestre sovrapposte**: osservazioni non indipendenti → gli "
             "intervalli di confidenza (Wilson) sono ottimistici.")
    L.append("- **Attribuzione single-news**: il realizzato riflette *tutte* le "
             "notizie della finestra, non solo quella classificata. Per questo la "
             "copertura distribuzionale (§1) e' piu' onesta dell'hit-rate puntuale.")
    L.append(f"- **No-call**: le previsioni con |mediana| < {FLAT_THRESHOLD}% sono "
             "escluse dall'hit-rate ma incluse nella copertura.")
    L.append("- **No look-ahead**: il realizzato di una scheda del giorno D e' "
             "misurato da D in avanti (cosa e' successo dopo la chiamata).\n")

    text = "\n".join(L)
    out_path.write_text(text, encoding="utf-8")
    html_path = _write_scorecard_html(text, out_path, f"{iso_year}-W{iso_week:02d}")
    print(f"[scorecard] scritta {out_path.name} + {html_path.name} "
          f"({n_total} previsioni mature, {n_cards} schede).")
    if open_browser:
        subprocess.run(["open", str(html_path)], check=False)


def cmd_run() -> None:
    cmd_backfill()
    cmd_evaluate()
    cmd_scorecard()


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("backfill", help="accoda al ledger le previsioni delle schede")
    sub.add_parser("evaluate", help="riempie le righe mature col realizzato dal DB")
    sc = sub.add_parser("scorecard", help="aggrega le metriche e scrive la scorecard")
    sc.add_argument("--open", action="store_true",
                    help="Apre la scorecard HTML nel browser (macOS)")
    sub.add_parser("run", help="backfill + evaluate + scorecard (job settimanale)")
    args = p.parse_args()

    if args.cmd == "scorecard":
        cmd_scorecard(open_browser=args.open)
    else:
        {"backfill": cmd_backfill, "evaluate": cmd_evaluate,
         "run": cmd_run}[args.cmd]()


if __name__ == "__main__":
    main()
