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

Dal 2026-09-23 (R09) ogni tabella DICHIARA nel titolo che uso ne fa la scheda:
  ### Event study — `BZ=F` [previsione]        la scheda ci costruisce una lettura
  ### Event study — `^GSPC` [descrittiva]      riportata, ma segno dichiarato inaffidabile
  ### Event study — `^TNX` [scenario: pool-b]  tabella alternativa dello stesso asset
Senza dichiarazione: `uso` vuoto = "non dichiarata" (tutte le righe precedenti).
Lo scenario entra nel `forecast_id`: due tabelle dello stesso asset/orizzonte non
collidono piu'.

VALUTAZIONE CONGELATA vs RICALCOLO
  evaluate  scrive una volta sola il realizzato con ancora/target (date e prezzi):
            e' il track record, non si riscrive.
  recheck   ricalcola dal DB attuale e mostra le differenze, in sola lettura.
Una scheda corretta dopo la registrazione (sha diverso): le righe ancora pendenti
restano congelate, come quelle gia' valutate. La revisione è segnalata con
`revised_at`, senza sostituire la chiamata originale.

ARCHITETTURA
------------
Un unico artefatto append-only: `daily_analysis/forecast_ledger.csv`. Una riga
per (scheda × asset × scenario × orizzonte), chiave `forecast_id`:
  - colonne "made"  scritte al momento del backfill/scrittura scheda;
  - colonne "eval"  riempite quando la previsione e' MATURA (il DB ha abbastanza
    giorni di borsa dopo l'ancora) — riusa event_study.compute_returns.

Sottocomandi:
  backfill   scansiona le schede e accoda al ledger le previsioni non ancora presenti
  evaluate   riempie le righe mature con realizzato / in_iqr / hit_dir / abs_error
  scorecard  aggrega le metriche e scrive daily_analysis/_scorecard/AAAA-Www.md
  run        backfill + evaluate + scorecard (usato dal job settimanale)
  recheck    ricalcola le righe valutate sul DB attuale (sola lettura)

Convenzioni metodologiche: identiche a event_study.py (anchor = primo trading
day >= data; T+N = N-esimo trading day dopo l'anchor; prezzo = COALESCE(adj_close,
close)). Il realizzato di una previsione fatta il giorno D usa D come evento:
l'orario di registrazione va confrontato con la chiusura dell'asset: la sola
data non certifica assenza di look-ahead.
"""

import argparse
import csv
import hashlib
import math
import re
import sqlite3
import subprocess
import sys
import os
import json
import tempfile
import fcntl
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import markdown

from bootstrap_market_data import DB_PATH
from event_study import compute_returns, load_price_series
from render_report import CSS, MD_EXTENSIONS


# --- Percorsi --------------------------------------------------------------
DAILY_DIR     = Path.home() / "Claude" / "mercati_finanza" / "daily_analysis"
LEDGER_PATH   = DAILY_DIR / "forecast_ledger.csv"
SCORECARD_DIR = DAILY_DIR / "_scorecard"

# Soglia "piatto": sotto questa |mediana| (in %) la scheda non si sbilancia su
# una direzione → esclusa dall'hit-rate direzionale, inclusa nella copertura.
FLAT_THRESHOLD = 0.10

# Cartella-giorno valida = nome strettamente AAAA-MM-GG (esclude _scorecard,
# *_manual_backup, ecc.).
DAY_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

FIELDS = [
    "forecast_id", "made_date", "slug", "card_path", "asset", "horizon",
    "scenario", "uso",
    "expected_median", "expected_mean", "hist_p25", "hist_p75",
    "n_analogues", "sentiment", "confidence", "directional",
    "card_sha", "recorded_at", "revised_at", "registration", "method_version", "ingestion_status",
    # colonne riempite in evaluate (congelate):
    "anchor_date", "anchor_price", "target_date", "target_price",
    "realized_return", "in_iqr", "hit_dir", "abs_error", "eval_date",
]

DECL_RE = re.compile(r"\[\s*(previsione|descrittiva|scenario\s*:\s*([^\]]+?))\s*\]", re.I)


# --- Parsing delle schede --------------------------------------------------

def _parse_pct(cell: str):
    """'+0.18%' / '-2.30%' / 'n/a' / '**6**' → float o None."""
    if cell is None:
        return None
    c = cell.strip().strip("*").strip()
    c = c.replace("%", "").replace("+", "").replace("−", "-").replace(",", ".").strip()
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


def parse_card(path: Path, issues: list | None = None) -> list[dict]:
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

    problems = []
    # Parse contiguous Markdown tables, never let a later table overwrite a prior one.
    table_text = re.sub(r"(?m)^\*\*(`[^`]+`[^\n]*)\*\*\s*$", r"### \1", text)
    table_text = re.sub(r"(?m)^\*\*([^\n]*\([A-Z0-9^][A-Z0-9^=._-]*\)[^\n]*)\*\*\s*$", r"### \1", table_text)
    blocks = re.split(r"(?m)^#{2,6}\s+", table_text)
    for blk in blocks:
        heading = blk.splitlines()[0] if blk.splitlines() else ""
        tickers = re.findall(r"`([A-Z0-9^][A-Z0-9^=._-]*)`", heading)
        if not tickers:
            tickers = re.findall(r"\(([A-Z0-9^][A-Z0-9^=._-]*)\)", heading)
        md = DECL_RE.search(heading)
        uso, scenario = "", "base"
        if md:
            if md.group(2):
                uso, scenario = "scenario", re.sub(r"\s+", "-", md.group(2).strip().lower())
            else:
                uso = md.group(1).lower()
        for table in re.findall(r"(?m)(?:^\|[^\n]*\n?)+", blk):
            lines = table.splitlines()
            if not any("T+" in ln for ln in lines) or ("T+" not in lines[0] and "mediana" not in table.lower()):
                continue
            if _table_row_cells(lines[0])[0].lower() in ("event", "event date", "data evento", "evento", "data"):
                continue  # per-event detail is not a forecast summary
            horizons = [int(h) for h in re.findall(r"T\+(\d+)", lines[0])]
            error = ""
            rows = {tk: {} for tk in tickers}
            if not horizons or not tickers or len(horizons) != len(set(horizons)):
                error = "asset/orizzonti non identificabili"
            else:
                for ln in lines[1:]:
                    cells = _table_row_cells(ln)
                    label = cells[0].replace("*", "").replace("`", "").strip()
                    targets = tickers
                    for tk in sorted(tickers, key=len, reverse=True):
                        if label.startswith(tk + " "):
                            targets, label = [tk], label[len(tk):].strip()
                            break
                    label = label.lower()
                    if label not in ("media", "mediana", "p25", "p75", "p25 / p75", "n"):
                        if "mediana" in label:
                            error = "mediana con asset non identificabile"
                        continue
                    if len(targets) > 1 and label != "n":
                        error = "statistica ambigua fra più asset"
                        break
                    if len(cells) != len(horizons) + 1:
                        error = "numero celle diverso dagli orizzonti"
                        break
                    labels = ["p25", "p75"] if label == "p25 / p75" else [label]
                    for j, name in enumerate(labels):
                        vals = []
                        for cell in cells[1:]:
                            parts = cell.split("/") if len(labels) == 2 else [cell]
                            if len(parts) != len(labels):
                                error = "quartili accorpati non validi"
                                break
                            raw = parts[j].strip().strip("*").strip()
                            v = _parse_pct(raw)
                            if ((v is None and raw.lower().rstrip("%") not in ("n/a", "—", "-", ""))
                                    or (v is not None and not math.isfinite(v))):
                                error = "valore non numerico o non finito"
                            vals.append(v)
                        for tk in targets:
                            if name in rows[tk]:
                                error = "statistica duplicata"
                            rows[tk][name] = vals
            table_entries = []
            if not error:
                for ticker, stats in rows.items():
                    if "mediana" not in stats:
                        error = "mediana assente per " + ticker
                        break
                    for i, hz in enumerate(horizons):
                        values = {k: v[i] for k, v in stats.items()}
                        med = values.get("mediana")
                        if med is None and values.get("n") == 0:
                            continue
                        if med is None:
                            error = "mediana mancante"
                            break
                        lo, hi, n = values.get("p25"), values.get("p75"), values.get("n")
                        if ((lo is None) != (hi is None) or
                                (lo is not None and not lo <= med <= hi) or
                                (n is not None and (n < 1 or n != int(n)))):
                            error = "quartili/N incoerenti"
                            break
                        table_entries.append({
                            "made_date": made_date, "slug": slug, "card_path": rel_path,
                            "asset": ticker, "horizon": hz, "scenario": scenario, "uso": uso,
                            "expected_median": med, "expected_mean": values.get("media"),
                            "hist_p25": lo, "hist_p75": hi,
                            "n_analogues": int(n) if n is not None else "",
                            "sentiment": sentiment, "confidence": confidence,
                            "directional": int(abs(med) >= FLAT_THRESHOLD),
                        })
            if error:
                problems.append(f"{rel_path}: {heading}: {error}")
            else:
                entries.extend(table_entries)
    # An ambiguous duplicate is not a second independent forecast.
    counts = {}
    for e in entries:
        counts[_key(e)] = counts.get(_key(e), 0) + 1
    duplicate = {k for k, n in counts.items() if n > 1}
    if duplicate:
        problems.append(f"{rel_path}: asset/orizzonte ripetuto senza scenario distinto")
        entries = [e for e in entries if _key(e) not in duplicate]
    if issues is not None:
        issues.extend(problems)
    else:
        for problem in problems:
            print("[quarantena] " + problem, file=sys.stderr)
    for e in entries:
        e["forecast_id"] = _key(e)
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
        rows = list(csv.DictReader(fp))
    # Righe precedenti a R09: nessuno scenario = tabella principale. Cosi' la
    # loro chiave coincide con quella che la stessa scheda produce oggi.
    for r in rows:
        r["scenario"] = r.get("scenario") or "base"
        r["forecast_id"] = r.get("forecast_id") or _key(r)
    return rows


def write_ledger(rows: list[dict]) -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    def sort_key(r):
        return (r["made_date"], r["slug"], r["asset"], r["scenario"], int(r["horizon"]))
    rows = sorted(rows, key=sort_key)
    with tempfile.NamedTemporaryFile(mode="w", newline="", encoding="utf-8",
                                     dir=LEDGER_PATH.parent, delete=False) as fp:
        w = csv.DictWriter(fp, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
        tmp = fp.name
    os.replace(tmp, LEDGER_PATH)


def _key(r: dict) -> str:
    """forecast_id: una previsione = scheda × asset × scenario × orizzonte."""
    return (f"{r['made_date']}/{r['slug']}/{r['asset']}/"
            f"{r.get('scenario') or 'base'}/T+{r['horizon']}")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


# --- Sottocomandi ----------------------------------------------------------

def cmd_backfill(day=None, live=False, skip=()) -> None:
    existing = load_ledger()
    by_card: dict = {}
    for r in existing:
        by_card.setdefault(r["card_path"], []).append(r)
    seen = {r["forecast_id"] for r in existing}
    today = date.today().isoformat()
    added = frozen = undeclared = 0
    version_files = [Path(__file__), Path(__file__).with_name('analogues.py'),
                     Path(__file__).with_name('event_study.py'),
                     Path(__file__).with_name('PHASE5_RUNBOOK.md'),
                     Path(__file__).with_name('subtheme_taxonomy.yaml'),
                     Path(__file__).with_name('news_card_template.md'),
                     Path(__file__).with_name('run_daily_analysis.sh')]
    version = hashlib.sha256(b''.join(p.read_bytes() for p in version_files)).hexdigest()[:12] if live else 'unknown'

    for card in discover_cards():
        if (day and card.parent.name != day) or card in skip:
            continue
        issues = []
        entries = parse_card(card, issues=issues)
        for old in by_card.get(str(card.relative_to(DAILY_DIR)), []):
            if old.get("registration") != "live":
                old["ingestion_status"] = "quarantine" if issues else "ok"
        if issues:
            for issue in issues:
                print("[quarantena] " + issue, file=sys.stderr)
            continue
        sha = _sha(card)
        new = {}
        for e in entries:
            if e["forecast_id"] in new:
                # Stesso asset/scenario due volte: vince la prima (come prima di
                # R09). Nelle schede nuove va dichiarato lo scenario.
                if e["uso"]:
                    print(f"[backfill] ⚠ {e['card_path']}: tabella {e['asset']} "
                          f"ripetuta senza scenario distinto → tenuta la prima")
                continue
            new[e["forecast_id"]] = e

        # Righe gia' registrate di questa scheda: correzione o no?
        for r in by_card.get(str(card.relative_to(DAILY_DIR)), []):
            if not r.get("card_sha"):
                r["card_sha"] = sha      # riga pre-R09: questa e' la versione di riferimento
                continue
            if r["card_sha"] == sha:
                continue
            # First registered forecast stays immutable even before evaluation.
            if not r.get("revised_at"):
                r["revised_at"] = datetime.now().astimezone().isoformat()
                frozen += 1

        for fid, e in new.items():
            if fid in seen:
                continue
            for k in FIELDS:
                e.setdefault(k, "")
            e["card_sha"] = sha
            e["recorded_at"] = datetime.now().astimezone().isoformat()
            e["registration"] = "live" if live and card.parent.name == today else "recovered"
            e["ingestion_status"] = "ok"
            e["method_version"] = version if e["registration"] == "live" else "unknown"
            if e["registration"] == "live":
                methods = DAILY_DIR / '_forecast_methods'
                methods.mkdir(exist_ok=True)
                method = methods / f'{version}.json'
                if not method.exists():
                    method.write_text(json.dumps({p.name: p.read_text() for p in version_files}, ensure_ascii=False))
            snapshots = card.parent / "_forecast_sources"
            snapshots.mkdir(exist_ok=True)
            snapshot = snapshots / f"{card.stem}-{sha}.md"
            if not snapshot.exists():
                snapshot.write_bytes(card.read_bytes())
            existing.append(e)
            seen.add(fid)
            added += 1
            undeclared += not e["uso"]

    write_ledger(existing)
    print(f"[backfill] righe nel ledger: {len(existing)} (+{added} nuove, di cui "
          f"{undeclared} senza dichiarazione d'uso). Schede corrette: {frozen} righe "
          f"lasciate congelate. File: {LEDGER_PATH}")


def cmd_evaluate() -> None:
    rows = load_ledger()
    if not rows:
        print("[evaluate] ledger vuoto — esegui prima 'backfill'.")
        return

    # Raggruppa per (asset, made_date) le righe non ancora valutate.
    pending = [r for r in rows if not r.get("realized_return") and r.get("uso") != "ritirata" and r.get("ingestion_status") != "quarantine"]
    if not pending:
        print("[evaluate] nessuna previsione in attesa di valutazione.")
        return

    today = date.today().isoformat()
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
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
                    res = compute_returns(conn, asset, [ed], [1, 3, 5, 10], as_of=date.today())
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

            t = pe["targets"][hz]
            r["anchor_date"] = pe["anchor_date"].isoformat()
            r["anchor_price"] = f"{pe['anchor_price']:.6g}"
            r["target_date"] = t["target_date"].isoformat()
            r["target_price"] = f"{t['target_price']:.6g}"
            r["realized_return"] = f"{realized:.4f}"
            if p25 is not None and p75 is not None:
                lo, hi = min(p25, p75), max(p25, p75)
                r["in_iqr"] = 1 if lo <= realized <= hi else 0
            if med is not None and abs(med) >= FLAT_THRESHOLD and realized != 0:
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


def _spearman(xs: list[float], ys: list[float]):
    # Spearman = Pearson sui ranghi (evita la dipendenza da scipy che pandas
    # richiederebbe con method="spearman").
    if len(xs) < 3:
        return None
    rx = pd.Series(xs).rank()
    ry = pd.Series(ys).rank()
    s = rx.corr(ry, method="pearson")
    return None if pd.isna(s) else float(s)


def _pct(x):
    return "n/a" if x is None else f"{x * 100:.0f}%"


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


def metric_summary(rows):
    """Same denominator for system and fixed-sign diagnostics; zero is not down."""
    h = [r for r in rows if abs(float(r["expected_median"])) >= FLAT_THRESHOLD
         and float(r["realized_return"]) != 0]
    bands = [r for r in rows if r.get("hist_p25") not in ("", None)
             and r.get("hist_p75") not in ("", None)]
    avg = lambda xs: sum(xs) / len(xs) if xs else None
    return {
        "n_hit": len(h), "n_band": len(bands),
        "hit": avg([(float(r["expected_median"]) > 0) ==
                    (float(r["realized_return"]) > 0) for r in h]),
        "up": avg([float(r["realized_return"]) > 0 for r in h]),
        "down": avg([float(r["realized_return"]) < 0 for r in h]),
        "coverage": avg([float(r["hist_p25"]) <= float(r["realized_return"]) <=
                         float(r["hist_p75"]) for r in bands]),
        "width": avg([float(r["hist_p75"]) - float(r["hist_p25"]) for r in bands]),
    }


def historical_baseline(prices, cutoff, horizon):
    """Last 252 complete daily outcomes ending before emission; at least 60."""
    past = prices[prices.index < pd.Timestamp(cutoff)].tail(252 + horizon)
    returns = ((past.shift(-horizon) / past - 1) * 100).replace(
        [float('inf'), float('-inf')], float('nan')).dropna()
    if len(returns) < 60:
        return None
    return dict(expected_median=float(returns.median()),
                hist_p25=float(returns.quantile(.25)), hist_p75=float(returns.quantile(.75)))


def cmd_audit(day=None, require_declared=False, bad=None):
    """Read-only ingestion inventory; malformed/ambiguous tables stay explicit."""
    failed = 0
    for card in discover_cards():
        if day and card.parent.name != day:
            continue
        issues = []
        entries = parse_card(card, issues=issues)
        if require_declared:
            if any(e['made_date'] != card.parent.name for e in entries):
                issues.append(f"{card.name}: Data analisi diversa dalla cartella-giorno")
            if any(not e['uso'] for e in entries):
                issues.append(f"{card.name}: dichiara l'uso di ogni tabella")
            if any(e['uso'] == 'previsione' and (not e['n_analogues'] or e['n_analogues'] < 10) for e in entries):
                issues.append(f"{card.name}: N<10 o assente; usa [descrittiva]")
        abstention = re.search(r"(?mi)^\*\*Motivo astensione\*\*:\s*\S[^\n]*", card.read_text())
        if not entries and not issues and not abstention:
            issues.append(f"{card.relative_to(DAILY_DIR)}: nessun risultato acquisibile")
        for issue in issues:
            print("QUARANTENA " + issue)
        failed += bool(issues)
        if issues and bad is not None:
            bad.append(card)
        if day and not issues:
            print(f"OK {card.name}: {len(entries)} righe")
    print(f"[audit] schede da verificare: {failed}")
    return failed


def cmd_scorecard(open_browser: bool = False) -> None:
    all_rows = load_ledger()
    matured = [r for r in all_rows if r.get("realized_return")
               and r.get("uso") not in ("ritirata", "scenario")
               and r.get("ingestion_status") != "quarantine"]
    active = [r for r in matured if r.get("uso") == "previsione"]
    L = [f"# Scorecard previsioni — {date.today().isocalendar().year}-W{date.today().isocalendar().week:02d}",
         f"\n_Generata: {datetime.now().isoformat(timespec='seconds')}_\n",
         "## In sintesi\n",
         "Il riepilogo distingue previsioni attive, descrizioni e recupero storico. "
         "Nessun asset è promosso automaticamente a affidabile. Sempre-su/sempre-giù "
         "sono controlli sullo stesso campione, non strategie validate. "
         "Copertura della banda e precisione direzionale misurano cose diverse.\n"]
    live = [r for r in active if r.get("registration") == "live"]
    sm = metric_summary(live)
    L.append(f"**Previsioni attive registrate dal flusso giornaliero:** {len(live)} mature, "
             f"{len({r['made_date'] for r in live})} giornate. "
             f"Hit-rate {_pct(sm['hit'])} su N={sm['n_hit']}; "
             f"sempre-su {_pct(sm['up'])}, sempre-giù {_pct(sm['down'])}. "
             "La registrazione prova l'ora di acquisizione, non da sola l'assenza di "
             "look-ahead: confrontare l'orario di emissione con la chiusura dell'asset.\n")
    L.append(f"Righe escluse per ingestione ambigua: {sum(r.get('ingestion_status') == 'quarantine' for r in all_rows)}. "
             "Dettaglio: `forecast_tracking.py audit`.\n")
    L.append("Campioni piccoli, righe correlate e selezione dei casi impediscono di "
             "interpretare differenze di pochi punti come un vantaggio dimostrato.\n")
    L.append("## 0-bis. Uso e provenienza\n")
    L.append("| Uso / provenienza | Righe mature | Giorni | Hit-rate | N hit | Sempre su | Sempre giù | Copertura | N bande |")
    L.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    groups = {}
    for r in matured:
        key = (r.get("uso") or "non dichiarata", r.get("registration") or "legacy")
        groups.setdefault(key, []).append(r)
    def group_line(label, sub):
        m = metric_summary(sub)
        return (f"| {label} | {len(sub)} | {len({r['made_date'] for r in sub})} | "
                f"{_pct(m['hit'])} | {m['n_hit']} | {_pct(m['up'])} | {_pct(m['down'])} | "
                f"{_pct(m['coverage'])} | {m['n_band']} |")
    for key, sub in sorted(groups.items()):
        L.append(group_line(' / '.join(key), sub))
    L.extend(["", "## 1. Coorti di emissione e versione\n",
              "Le date separano i periodi, non ricostruiscono versioni mancanti. "
              "Le tabelle recuperate oggi restano retrospettive.\n",
              "| Settimana / versione | Righe mature | Giorni | Hit-rate | N hit | Sempre su | Sempre giù | Copertura | N bande |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|"])
    cohorts = {}
    for r in active:
        iso = date.fromisoformat(r['made_date']).isocalendar()
        key = f"{iso.year}-W{iso.week:02d} / {r.get('method_version') or 'non registrata'}"
        cohorts.setdefault(key, []).append(r)
    for key, sub in sorted(cohorts.items()):
        L.append(group_line(key, sub))
    L.extend(["", "## 2. Maturazione delle previsioni attive\n",
              "| Orizzonte | Registrate | Mature | Astensioni sul segno fra le mature |",
              "|---|---:|---:|---:|"])
    for hz in sorted({int(r['horizon']) for r in all_rows}):
        sub = [r for r in all_rows if r.get('uso') == 'previsione' and r.get('ingestion_status') != 'quarantine' and int(r['horizon']) == hz]
        mature = [r for r in sub if r.get('realized_return')]
        L.append(f"| T+{hz} | {len(sub)} | {len(mature)} | "
                 f"{sum(abs(float(r['expected_median'])) < FLAT_THRESHOLD for r in mature)} |")
    L.extend(["", "## 5. Confronto per asset e orizzonte — previsioni attive\n",
              "## 5-bis. Su quali ASSET prevediamo meglio?\n",
              "Solo tabelle attive; descrittive e legacy senza uso sono sopra. "
              "IC misurato separatamente per ticker e orizzonte. "
              "N unici conta giorni-ancora per asset/orizzonte: resta dipendenza fra "
              "finestre sovrapposte. Nessun intervallo Wilson o semaforo di affidabilità.\n",
              "| Asset | Orizzonte | N righe | N unici | Hit-rate | N hit | Sempre su | Sempre giù | IC | Copertura | N bande | Ampiezza banda (pp) |",
              "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"])
    grouped = {}
    for r in active:
        grouped.setdefault((r['asset'], int(r['horizon'])), []).append(r)
    for (asset, hz), sub in sorted(grouped.items()):
        m = metric_summary(sub)
        ic = _spearman([float(r['expected_median']) for r in sub],
                       [float(r['realized_return']) for r in sub])
        uniques = len({r.get('anchor_date') or r['made_date'] for r in sub})
        L.append(f"| {asset} | T+{hz} | {len(sub)} | {uniques} | {_pct(m['hit'])} | "
                 f"{m['n_hit']} | {_pct(m['up'])} | {_pct(m['down'])} | "
                 f"{ic if ic is not None else 'n/a'} | {_pct(m['coverage'])} | "
                 f"{m['n_band']} | {m['width'] if m['width'] is not None else 'n/a'} |")
    L.extend(["", "## 6. Riferimento storico senza selezione di notizie\n",
              "Ultime 252 finestre disponibili del medesimo asset/orizzonte, tutte concluse "
              "prima del giorno di emissione; minimo 60. Ricostruito dal DB attuale: "
              "rispetta il cutoff dei prezzi, ma non certifica le vintage originarie. "
              "Confronto su identiche righe attive; hit-rate solo dove entrambi i metodi "
              "sono direzionali. Nessuna ottimizzazione o promozione automatica.\n",
              "| Asset | T+ | N coppie | N segno | Hit sistema / rif. | MAE sistema / rif. (pp) | Copertura sistema / rif. | Ampiezza sistema / rif. (pp) | N bande |",
              "|---|---|---:|---:|---|---|---|---|---:|"])
    with sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True) as conn:
        prices_by_asset = {}
        cache = {}
        for (asset, hz), sub in sorted(grouped.items()):
            if asset not in prices_by_asset:
                try:
                    prices_by_asset[asset] = load_price_series(conn, asset)
                except ValueError:
                    prices_by_asset[asset] = None
            prices = prices_by_asset[asset]
            if prices is None:
                L.append(f"| {asset} | {hz} | 0 | 0 | serie assente | — | — | — | 0 |")
                continue
            pairs = []
            for r in sub:
                key = (asset, hz, r['made_date'])
                if key not in cache:
                    cache[key] = historical_baseline(prices, date.fromisoformat(r['made_date']), hz)
                if cache[key] is not None:
                    pairs.append((r, dict(cache[key], realized_return=r['realized_return'])))
            if not pairs:
                L.append(f"| {asset} | {hz} | 0 | 0 | storico insufficiente | — | — | — | 0 |")
                continue
            directional = [(r, b) for r, b in pairs if float(r['realized_return']) != 0
                           and abs(float(r['expected_median'])) >= FLAT_THRESHOLD
                           and abs(b['expected_median']) >= FLAT_THRESHOLD]
            band_pairs = [(r, b) for r, b in pairs if r.get('hist_p25') not in ('', None)
                          and r.get('hist_p75') not in ('', None)]
            h = [metric_summary([pair[i] for pair in directional])['hit'] for i in (0, 1)]
            m = [metric_summary([pair[i] for pair in band_pairs]) for i in (0, 1)]
            mae = [sum(abs(float(pair[i]['expected_median']) - float(pair[i]['realized_return']))
                       for pair in pairs) / len(pairs) for i in (0, 1)]
            width = ' / '.join('n/a' if x['width'] is None else f"{x['width']:.2f}" for x in m)
            L.append(f"| {asset} | {hz} | {len(pairs)} | {len(directional)} | "
                     f"{_pct(h[0])} / {_pct(h[1])} | {mae[0]:.2f} / {mae[1]:.2f} | "
                     f"{_pct(m[0]['coverage'])} / {_pct(m[1]['coverage'])} | {width} | {len(band_pairs)} |")
    L.extend(["", "## Caveat\n",
              "- Le bande p25–p75 sono distribuzioni storiche, non intervalli di confidenza della mediana.",
              "- Sempre-su/sempre-giù sono confronti descrittivi; scegliere il migliore dopo gli esiti è retrospettivo.",
              "- Le osservazioni sono correlate; nessuna numerosità di righe certifica indipendenza.",
              "- L'ancora è la prima chiusura alla data dell'analisi o dopo, non la chiusura precedente all'annuncio.",
              "- Il movimento incorpora tutte le notizie della finestra, non soltanto quella della scheda.",
              "- Audit ingestione: `forecast_tracking.py audit` elenca tabelle ambigue o non lette."])
    SCORECARD_DIR.mkdir(parents=True, exist_ok=True)
    iso = date.today().isocalendar()
    out_path = SCORECARD_DIR / f"{iso.year}-W{iso.week:02d}.md"
    text = '\n'.join(L) + '\n'
    # Preserve an earlier scorecard before publishing a revised methodology.
    if out_path.exists() and out_path.read_text() != text:
        archive = SCORECARD_DIR / '_history'
        archive.mkdir(exist_ok=True)
        old = out_path.read_bytes()
        (archive / f"{out_path.stem}-{hashlib.sha256(old).hexdigest()[:12]}.md").write_bytes(old)
    out_path.write_text(text, encoding='utf-8')
    html = _write_scorecard_html(text, out_path, out_path.stem)
    print(f"[scorecard] {out_path}")
    if open_browser:
        subprocess.run(['open', str(html)], check=False)


def cmd_recheck() -> None:
    """Ricalcolo su dati revisionati: confronta il realizzato congelato con quello
    che il DB darebbe oggi. Non scrive nulla: il ledger resta il track record."""
    rows = [r for r in load_ledger() if r.get("realized_return")]
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    cache: dict = {}
    diffs, n = [], 0
    try:
        for r in rows:
            ckey = (r["asset"], r["made_date"])
            if ckey not in cache:
                try:
                    res = compute_returns(conn, r["asset"],
                                          [date.fromisoformat(r["made_date"])], [1, 3, 5, 10])
                    cache[ckey] = res["per_event"][0] if res["per_event"] else None
                except ValueError:
                    cache[ckey] = None
            pe = cache[ckey]
            now = pe["returns"].get(int(r["horizon"])) if pe else None
            if now is None:
                continue
            n += 1
            d = now - float(r["realized_return"])
            if abs(d) >= 0.01:
                t = pe["targets"][int(r["horizon"])]
                diffs.append((abs(d), r, now, pe["anchor_date"].isoformat(),
                              t["target_date"].isoformat()))
    finally:
        conn.close()
    print(f"[recheck] ricalcolate {n} righe valutate: {len(diffs)} differiscono "
          f"di almeno 0,01 punti dal valore congelato.")
    for _, r, now, anc, tgt in sorted(diffs, key=lambda x: -x[0])[:15]:
        congelate = (f"ancora {r['anchor_date']} → {r.get('target_date') or '?'}"
                     if r.get("target_date") else "date non registrate (pre-R09)")
        print(f"  {r['forecast_id']}: congelato {float(r['realized_return']):+.2f}% "
              f"({congelate}) · oggi {now:+.2f}% (ancora {anc} → {tgt})")


def cmd_run() -> None:
    cmd_backfill()
    cmd_evaluate()
    cmd_scorecard()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("backfill", "evaluate", "run", "recheck", "scorecard", "audit", "register"):
        cmd = sub.add_parser(name)
        if name in ("register", "audit"):
            cmd.add_argument("--date", type=date.fromisoformat, required=name == "register")
        if name == "scorecard":
            cmd.add_argument("--open", action="store_true")
    args = parser.parse_args()
    if args.cmd == 'audit':
        raise SystemExit(bool(cmd_audit(str(args.date) if args.date else None)))
    if args.cmd == 'recheck':
        cmd_recheck()
        return
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    with (DAILY_DIR / '_forecast.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if args.cmd == 'register':
            day = str(args.date)
            # Le schede ambigue restano fuori dal ledger, le altre si registrano:
            # una tabella malformata non deve fermare la consegna del giorno.
            bad = []
            cmd_audit(day, require_declared=True, bad=bad)
            cmd_backfill(day=day, live=True, skip=set(bad))
            if bad:
                raise SystemExit(f"Registrazione parziale: {len(bad)} schede escluse, "
                                 "correggerle e rilanciare 'register'")
        elif args.cmd == 'scorecard':
            cmd_scorecard(open_browser=args.open)
        else:
            {'backfill': cmd_backfill, 'evaluate': cmd_evaluate, 'run': cmd_run}[args.cmd]()


if __name__ == '__main__':
    main()
