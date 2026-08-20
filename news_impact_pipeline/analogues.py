#!/usr/bin/env python3
"""
analogues.py — Opzione B: libreria di episodi storici per l'event study.

Problema (scorecard W25): ogni previsione usa N≈5 analoghi scelti a mano → bande
inaffidabili. Qui costruiamo una RISERVA riutilizzabile di episodi datati, raccolti
dal lavoro già fatto (schede giornaliere + ricerche KB), così l'event study può
pescare 20-40 analoghi per tema invece di 5.

⚠ Principio: più episodi aiutano SOLO se restano analoghi. `find` filtra per tema
(e opzionalmente direzione e no-look-ahead), non mescola tutto.

Sottocomandi:
  build                          (ri)costruisce knowledge_base/_episodes.yaml
  find --theme X [--direction d] [--before YYYY-MM-DD]
                                 stampa le date-episodio (CSV pronto per --events)
  stats                          conteggio episodi per tema
"""

import argparse
import re
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

import yaml

DAILY_DIR = Path.home() / "Claude" / "mercati_finanza" / "daily_analysis"
KB_DIR = Path.home() / "Claude" / "mercati_finanza" / "knowledge_base"
LIB_PATH = KB_DIR / "_episodes.yaml"   # prefisso "_" → build_catalog lo ignora
TAXONOMY_PATH = Path(__file__).with_name("subtheme_taxonomy.yaml")

DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
DAY_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Blocco di metadata in coda alle ricerche KB: ```yaml ... ``` (template Design
# Doc §5.2). Contiene date che NON sono episodi — `date_compiled`, `time_window`
# e soprattutto i confini di `regime_phases` — e che finivano in libreria come
# eventi fasulli (67 al 2026-08-15: 2023-01-01, 2024-06-30, 2025-01-26,
# perfino 2026-12-31, una data futura). Erano entrate anche nei pool reali:
# il `--events` di 2026-08-15/news_04 ne conteneva cinque.
KB_META_RE = re.compile(r"\n```yaml\b.*?(?:\n```|\Z)", re.S)

# Intervallo di date: «2014-03-01 to 2022-01-31», «2025-03-01 → presente».
# Gli estremi di un intervallo sono CONFINI DI REGIME, non eventi. Le §5 delle
# ricerche KB ripetono in prosa le `regime_phases` del blocco YAML, quindi
# ripulire solo il blocco non basta.
RANGE_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2})\s*(?:to|a|al|fino a|→|->|-{1,2}|–|—|\.{2,})\s*"
    r"(\d{4}-\d{2}-\d{2}|presente|present|oggi|now)", re.I)


def _range_only_dates(text: str) -> set[str]:
    """Date che nel documento compaiono SOLO come estremo di un intervallo.
    Una data che appare anche altrove (riga del catalogo episodi, prosa) resta:
    l'esclusione vale per i confini, non per gli eventi che capitano di ricadervi."""
    in_range: dict[str, int] = {}
    for m in RANGE_RE.finditer(text):
        for g in m.groups():
            if g and DATE_RE.fullmatch(g):
                in_range[g] = in_range.get(g, 0) + 1
    return {d for d, n in in_range.items() if n >= len(re.findall(re.escape(d), text))}


def normalize_direction(sentiment: str) -> str:
    """Sentiment libero della scheda → segno grezzo per il matching."""
    s = (sentiment or "").lower()
    if any(k in s for k in ("hawkish", "bear", "risk-off", "risk_off", "disinflat", "negativ")):
        return "neg"
    if any(k in s for k in ("dovish", "bull", "risk-on", "risk_on", "positiv")):
        return "pos"
    return "neutral"


# Direzione DATE-LOCALE (2026-08-19). Stesso principio di `subthemes_local`: la
# direzione di un episodio va letta dal testo attorno a QUELLA data, non ereditata
# dalla scheda che l'ha citata.
# Il bug che risolve: `harvest_card` estrae UN solo `sentiment` per scheda e
# `cmd_build` lo applicava a TUTTE le date della scheda — comprese le 20-30 date
# storiche citate come analoghi, che non hanno nulla a che vedere col segno della
# notizia di oggi. Misurato il 2026-08-19: 367 episodi su 844 (43%) portavano 2 o
# 3 direzioni insieme, e il filtro `--direction` diventava nominale
# (macro_data/activity_growth: 43 episodi, 35 pos, 42 neg, 35 con ENTRAMBE;
# regulatory/tariff_escalation: 36 episodi e ZERO pos, perché nessuna scheda
# distensiva li aveva mai citati).
# Frequenze misurate su 2.880 contesti date-locali prima di scrivere i pattern:
#   neg: shock 284 · hawkish 195 · escalation 189 · attacc 136 · miss 91 · sanzion 57
#        selloff 36 · invasione 31 · sell-off 28 · crolla 25 · risk-off 24 · crollo 23
#   pos: dovish 67 · rally 51 · rimbalz 36 · accordo 32 · beat 32 · allenta 22
#        tregua 21 · riapertura 16 · risk-on 16 · distension 12
# ESCLUSI di proposito: 'tagli' (103) e 'dazi' (54) sono marcatori di TEMA, non di
# verso ('taglio dei tassi' è dovish ma 'tagli alla produzione' no); '\bmiss\b' è
# ancorato perché senza confini catturava 'missile', frequentissimo nelle schede
# geopolitiche.
DIRECTION_PATTERNS = {
    "neg": [re.compile(p, re.I) for p in (
        r"\bshock\b", r"hawkish", r"escalation|escalat", r"attacc\w+", r"\bmiss\b",
        r"sanzion\w+", r"sell-?off", r"invasion\w+", r"crolla|crollo|tonfo",
        r"risk-?off", r"stretta", r"contrazione", r"recession\w+",
        r"sotto le attese", r"delusion\w+", r"default|fallimento", r"panico",
    )],
    "pos": [re.compile(p, re.I) for p in (
        r"dovish", r"\brally\b", r"rimbalz\w+", r"accordo|intesa", r"\bbeat\b",
        r"allenta\w*", r"tregua", r"riapertura", r"risk-?on", r"distension\w+",
        r"sollievo", r"sopra le attese", r"sorpresa positiva", r"revoca|esenzione",
    )],
}


# ---------------------------------------------------------------------------
# Blocco episodi DICHIARATO (2026-08-19)
#
# Correzione a monte della classe di bug che ha prodotto una lacuna quasi ogni
# giorno dal 5 al 19 agosto 2026: la libreria *indovinava* gli attributi di un
# episodio applicando regex alla prosa, e ogni attributo nuovo nasceva a livello
# di documento per poi essere corretto settimane dopo (sotto-temi il 15/08,
# intestazione il 18/08, direzione il 19/08 — quest'ultima già diagnosticata
# correttamente il 05/08). Misurato il 19/08: il 38% degli episodi non aveva
# alcun sotto-tema date-locale e il 53% nessuna direzione date-locale.
#
# Qui la scheda DICHIARA i suoi episodi in una tabella a colonne fisse, e la
# libreria legge campi invece di interpretare frasi. Formato (v. news_card_template.md):
#
#   | Data | Verso | Meccanismo | Descrizione |
#   |---|---|---|---|
#   | `2018-03-22` | neg | tariff_escalation | Section 301 sulla Cina |
#
# Il verso ammette pos/neg/neutral (o entrambi separati da virgola, se la giornata
# lo era davvero). Il meccanismo è una lista di token canonici della tassonomia.
# Le schede scritte prima di questa data non hanno il blocco: per loro resta il
# percorso euristico, quindi la migrazione è incrementale e non rompe nulla.
DECLARED_ROW_RE = re.compile(
    r"^\s*\|\s*`?(\d{4}-\d{2}-\d{2})`?\s*\|"      # data
    r"\s*([a-zA-Z, /]*)\s*\|"                     # verso
    r"\s*([^|]*)\s*\|",                           # meccanismo (token canonici)
    re.M)
_VERSO_MAP = {"pos": "pos", "positivo": "pos", "positive": "pos", "bull": "pos",
              "neg": "neg", "negativo": "neg", "negative": "neg", "bear": "neg",
              "neutral": "neutral", "neutro": "neutral"}


def declared_episodes(text: str) -> dict[str, tuple[set[str], set[str]]]:
    """Episodi dichiarati nella scheda: {data: (versi, token di meccanismo)}.

    Ignora le righe di intestazione/separatore della tabella e le righe il cui
    verso non è riconoscibile: meglio ricadere sull'euristica che registrare un
    segno inventato."""
    out: dict[str, tuple[set[str], set[str]]] = {}
    for d, verso_raw, mecc_raw in DECLARED_ROW_RE.findall(text):
        versi = {_VERSO_MAP[v] for v in
                 (x.strip().lower() for x in re.split(r"[,/]", verso_raw))
                 if v in _VERSO_MAP}
        if not versi:
            continue                      # riga di tabella non-episodio, o verso illeggibile
        tokens = {lbl for t in re.split(r"[,/]", mecc_raw or "") if (lbl := _norm_label(t))}
        prev_v, prev_t = out.get(d, (set(), set()))
        out[d] = (prev_v | versi, prev_t | tokens)
    return out


def local_direction(text: str, d: str) -> set[str]:
    """Direzioni desumibili dal testo attorno alla data `d`.

    Può restituire l'insieme vuoto (nessun marcatore: l'episodio resta senza
    direzione locale e il filtro ricade sul livello di scheda) oppure entrambe le
    direzioni (riga genuinamente ambivalente: la teniamo, non la forziamo)."""
    ctx = _contexts(text, d)
    if not ctx.strip():
        return set()
    return {sign for sign, pats in DIRECTION_PATTERNS.items()
            if any(p.search(ctx) for p in pats)}


def _field(text: str, name: str) -> str:
    m = re.search(rf"\|\s*`{name}`\s*\|\s*([^\|<\n]+)", text)
    return m.group(1).strip() if m else ""


def _norm_label(t: str) -> str:
    """Etichetta di sotto-tema in forma canonica: minuscolo, separatori → '_'.

    Senza questo `ai capex`, `ai-capex` e `ai_capex` erano tre etichette distinte
    (tutte e tre presenti in libreria al 2026-08-15), e lo stesso per
    `valuation-derisking`/`valuation_derisking` e `semiconductor cycle`/
    `semiconductor_cycle`: il filtro `--subtheme` ne prendeva una sola."""
    t = t.strip().strip("`").lower()
    # Le parentesi spaiate delle annotazioni di tema ('geopolitical (middle east')
    # producevano token spazzatura come `iran)` e `geopolitical_(middle_east`.
    t = re.sub(r"[()\[\]]", "", t)
    return re.sub(r"_+", "_", re.sub(r"[\s\-]+", "_", t)).strip("_")


def _split_subthemes(raw: str) -> set[str]:
    """'ecb_supply_shock_pivot, stagflation_dilemma' → {token normalizzati}."""
    return {lbl for t in re.split(r"[,/]", raw or "") if (lbl := _norm_label(t))}


# ---------------------------------------------------------------------------
# Etichette di sotto-tema DATE-LOCALI
#
# Lacuna dichiarata nell'analisi del 2026-08-15: i `sub_themes` di un documento
# venivano applicati a ogni data che il documento cita, quindi un'unica scheda
# con 27 analoghi spalmava le sue 3-4 etichette su 27 episodi. Su
# `structural_themes` questo portava 53 episodi su 58 ad avere `semis` e 52
# `ai_capex` → `find --subtheme` non discriminava e schede con domande diverse
# (finanziamento del capex vs ciclo della memoria) pescavano lo stesso pool.
#
# Qui le etichette vengono ricavate dal CONTESTO in cui la data compare (riga di
# tabella, bullet, paragrafo), non dall'intestazione del documento. Due fonti:
#   1. la tassonomia canonica in subtheme_taxonomy.yaml (pattern per tema);
#   2. i `sub_themes` dichiarati dal documento, ma solo quelli che compaiono
#      DAVVERO nel contesto locale.
# ---------------------------------------------------------------------------

def load_taxonomy() -> dict[str, dict[str, list[re.Pattern]]]:
    if not TAXONOMY_PATH.exists():
        return {}
    raw = yaml.safe_load(TAXONOMY_PATH.read_text(encoding="utf-8")) or {}
    return {theme: {lbl: [re.compile(p, re.I) for p in pats]
                    for lbl, pats in (labels or {}).items()}
            for theme, labels in raw.items()}


ARGS_RE = re.compile(r"^\s*--|--events\b|--ticker\b")
# Intestazione della scheda: `**Data analisi**: 2026-08-18`, `**Fonte**: ...`,
# `**Slug**: synchronised-long-end-selloff`. Va esclusa come le righe-argomento:
# lo slug è una collana di parole chiave che non descrive un episodio ma l'intera
# scheda, e finiva per etichettare la data di analisi con mezzo vocabolario
# (386 contesti su 2.944 — il 13,1% — contaminati, misurato il 2026-08-18).
HEADER_RE = re.compile(r"\*\*(data analisi|fonte|slug)\*\*", re.I)


def _contexts(text: str, d: str) -> str:
    """Testo attorno a ogni occorrenza della data `d`, tenendo solo le occorrenze
    che parlano di QUELLA data e di nessun'altra.

    Quattro esclusioni, tutte necessarie perché l'etichetta resti attribuibile:
    - righe di argomenti (`--events 2019-05-15,2022-10-07,...`, `--ticker ...`):
      elenchi di date senza testo, non descrivono nulla;
    - righe di intestazione (`**Data analisi**`, `**Fonte**`, `**Slug**`):
      descrivono la scheda intera, non un episodio;
    - righe con più di una data: la descrizione è ambigua fra le due;
    - estensione alle righe vicine solo se la riga è quasi vuota (bullet spezzato)
      e solo verso righe che non contengono a loro volta una data — senza questo
      vincolo le righe di una tabella di risultati si contaminano a vicenda e una
      riga «2025-04-04 (tariff shock)» etichettava anche l'episodio della riga
      sopra (148 attribuzioni spurie misurate al 2026-08-15)."""
    lines = text.splitlines()
    out = []
    for i, line in enumerate(lines):
        if d not in line or ARGS_RE.search(line) or HEADER_RE.search(line):
            continue
        if len(set(DATE_RE.findall(line))) > 1:
            continue
        chunk = line
        if len(line) < 60:
            neigh = [lines[j] for j in (i - 1, i + 1) if 0 <= j < len(lines)]
            chunk = " ".join([line] + [ln for ln in neigh
                                       if ln.strip() and not DATE_RE.search(ln)
                                       and not ARGS_RE.search(ln)
                                       and not HEADER_RE.search(ln)])
        out.append(chunk)
    return "\n".join(out)


def local_labels(text: str, d: str, theme: str, declared: set[str],
                 taxonomy: dict) -> set[str]:
    ctx = _contexts(text, d)
    if not ctx.strip():
        return set()
    found = set()
    for scope in ("_any", theme):
        for lbl, pats in (taxonomy.get(scope) or {}).items():
            if any(p.search(ctx) for p in pats):
                found.add(lbl)
    # Un'etichetta dichiarata dal documento vale localmente solo se le sue parole
    # sono presenti nel contesto della data (`hbm_memory` → "hbm memory"/"hbm").
    low = ctx.lower()
    for lbl in declared:
        words = [w for w in lbl.split("_") if len(w) > 2]
        if words and all(w in low for w in words):
            found.add(lbl)
    return found


# Ontologia canonica (Design Doc §6.1): il tema DEVE essere uno di questi.
THEMES = {"monetary_policy", "fiscal_policy", "geopolitical", "macro_data",
          "corporate_idiosyncratic", "regulatory", "commodity_energy",
          "financial_stability", "structural_themes"}


def _norm_theme(raw: str) -> str:
    """Normalizza il primary_theme di una scheda al valore canonico.

    Alcune schede annotano il tema tra parentesi ('monetary_policy (sub: china /
    pboc)', 'regulatory (tariff = misura commerciale)'): senza normalizzazione
    diventano TEMI-FANTASMA distinti e i loro episodi spariscono dal pool del tema
    vero (83 episodi silosati al 2026-07-29). Qui tagliamo l'annotazione e teniamo
    solo il token canonico; se non è in ontologia restituiamo '' (scartato)."""
    t = re.split(r"[(\[]", raw or "", 1)[0].strip().strip("`").lower()
    t = t.replace(" ", "_").replace("-", "_")
    return t if t in THEMES else ""


def harvest_card(path: Path) -> tuple[str, str, set[str], set[str], str]:
    """Da una scheda: (theme, sentiment, sub_themes, {date-episodio}). Le date-analogo
    vivono nei comandi `--events ...` e nei bullet `\\`YYYY-MM-DD\\`` della sezione
    episodi; la data della scheda ('**Data analisi**: ...') NON è in backtick → esclusa."""
    text = path.read_text(encoding="utf-8")
    raw_theme = _field(text, "primary_theme")
    theme = _norm_theme(raw_theme)
    sentiment = _field(text, "sentiment")
    subthemes = _split_subthemes(_field(text, "sub_themes"))
    # L'annotazione fra parentesi del tema ('(sub: china / pboc)') non va persa:
    # è informazione di sotto-tema, la recuperiamo invece di scartarla col taglio.
    extra = re.search(r"[(\[]([^)\]]*)[)\]]", raw_theme or "")
    if extra:
        subthemes |= {t for t in _split_subthemes(
            re.sub(r"^\s*sub\s*:", "", extra.group(1), flags=re.I)) if t}
    dates: set[str] = set()
    for ev in re.findall(r"--events\s+([0-9,\-]+)", text):
        dates.update(d for d in ev.split(",") if DATE_RE.fullmatch(d))
    dates.update(re.findall(r"`(\d{4}-\d{2}-\d{2})`", text))
    return theme, sentiment, subthemes, dates, text


def harvest_kb(path: Path) -> tuple[str, set[str], set[str], str]:
    """Da uno studio KB: (primary_theme, sub_themes, {ISO date citate nel testo},
    testo-senza-metadata). Le date in prosa sono analoghi curati dalla
    deep-research; quelle nel blocco YAML di coda NO (vedi KB_META_RE)."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"primary_theme:\s*([^\n]+)", text)
    theme = _norm_theme(m.group(1)) if m else ""
    ms = re.search(r"sub_themes:\s*\[([^\]]*)\]", text)
    subthemes = _split_subthemes(ms.group(1)) if ms else set()
    body = KB_META_RE.sub("\n", text)
    dates = set(DATE_RE.findall(body)) - _range_only_dates(body)
    return theme, subthemes, dates, body


def cmd_build():
    # chiave episodio = (date, theme); accumuliamo direzioni e fonti
    lib: dict = {}
    taxonomy = load_taxonomy()

    today = date.today().isoformat()

    def add(d, theme, direction, subthemes, local, source, dir_local=(), declared=False):
        if not theme or not DATE_RE.fullmatch(d):
            return
        if d > today:
            return   # una data futura non è un episodio: è un orizzonte citato nel testo
        key = (d, theme)
        e = lib.setdefault(key, {"date": d, "theme": theme, "directions": set(),
                                 "directions_local": set(),
                                 "subthemes": set(), "subthemes_local": set(),
                                 "sources": set(), "declared": False})
        if direction:
            e["directions"].add(direction)
        e["directions_local"].update(dir_local)
        if declared:
            e["declared"] = True
        e["subthemes"].update(subthemes)
        e["subthemes_local"].update(local)
        e["sources"].add(source)

    # 1) schede giornaliere (fonte primaria: episodi + direzione + sotto-temi)
    n_cards = 0
    for day in sorted(DAILY_DIR.iterdir()):
        if not (day.is_dir() and DAY_DIR_RE.match(day.name)):
            continue
        for card in sorted(day.glob("news_*.md")):
            n_cards += 1
            theme, sentiment, subthemes, dates, text = harvest_card(card)
            direction = normalize_direction(sentiment)
            decl = declared_episodes(text)
            for d in dates:
                # Se la scheda dichiara l'episodio, i suoi campi VINCONO sull'euristica:
                # sono date-locali per costruzione e non per inferenza. L'euristica
                # resta per le schede scritte prima del 2026-08-19.
                dec_v, dec_t = decl.get(d, (set(), set()))
                add(d, theme, direction, subthemes,
                    dec_t or local_labels(text, d, theme, subthemes, taxonomy),
                    f"card:{day.name}/{card.name}",
                    dec_v or local_direction(text, d),
                    declared=bool(dec_v))

    # 2) ricerche KB (esclude _prompts e file con prefisso _)
    n_kb = 0
    for md in sorted(KB_DIR.rglob("*.md")):
        if any(p.startswith("_") for p in md.relative_to(KB_DIR).parts):
            continue
        n_kb += 1
        theme, subthemes, dates, body = harvest_kb(md)
        for d in dates:
            add(d, theme, "", subthemes,
                local_labels(body, d, theme, subthemes, taxonomy),
                f"kb:{md.parent.name}",
                local_direction(body, d))

    episodes = []
    for e in sorted(lib.values(), key=lambda x: (x["theme"], x["date"])):
        dirs = sorted(d for d in e["directions"] if d)
        # Conserviamo TUTTE le direzioni osservate, non un singolo valore collassato.
        # Prima: 2+ direzioni sullo stesso (data,tema) → "mixed", che distruggeva
        # l'informazione — al 2026-08-10 erano 61 episodi su 102 in monetary_policy,
        # e solo 5 restavano taggati "pos": i pool dovish e hawkish finivano identici
        # (schede diverse, previsioni uguali al centesimo). Un giorno in cui sono
        # uscite sia una notizia hawkish sia una dovish è un analogo legittimo per
        # ENTRAMBE le direzioni: ora `find` fa match se la direzione richiesta è fra
        # quelle osservate. `direction` (singolare) resta per compatibilità/lettura.
        episodes.append({"date": e["date"], "theme": e["theme"],
                         "direction": (dirs[0] if len(dirs) == 1
                                       else ("mixed" if dirs else "")),
                         "directions": dirs,
                         "directions_local": sorted(e["directions_local"]),
                         "declared": bool(e.get("declared")),
                         "subthemes": sorted(e["subthemes"]),
                         "subthemes_local": sorted(e["subthemes_local"]),
                         "n_sources": len(e["sources"])})

    LIB_PATH.write_text(yaml.safe_dump(
        {"generated_at": datetime.now().isoformat(timespec="seconds"),
         "num_episodes": len(episodes), "episodes": episodes},
        sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"[analogues] {len(episodes)} episodi unici (date×tema) da {n_cards} schede "
          f"+ {n_kb} file KB → {LIB_PATH}")


def _load() -> list[dict]:
    if not LIB_PATH.exists():
        raise SystemExit("Libreria assente: lancia prima `analogues.py build`.")
    return yaml.safe_load(LIB_PATH.read_text(encoding="utf-8"))["episodes"]


def cmd_find(theme: str, direction: str | None, before: str | None,
             subtheme: list[str] | None, min_n: int, max_pool: int):
    eps = [e for e in _load() if e["theme"] == theme]
    if before:
        eps = [e for e in eps if e["date"] < before]   # no look-ahead
    note = ""
    if subtheme:
        wanted = [_norm_label(s) for s in subtheme]

        def _match(field):
            return [e for e in eps
                    if any(w in st for w in wanted for st in (e.get(field) or []))]

        # Degrado a tre livelli. `subthemes_local` sono etichette ricavate dal
        # contesto della singola data: discriminano davvero, ma esistono solo dove
        # la fonte descrive l'episodio (tabelle KB, bullet delle schede). Se sono
        # troppo poche si scende su `subthemes` (unione a livello di documento,
        # larga ma poco selettiva) e infine sul tema. Qualità prima, ma mai a
        # costo di N.
        strict = _match("subthemes_local")
        loose = _match("subthemes")
        lbl = ",".join(subtheme)
        if len(strict) >= min_n:
            eps = strict
            note = f" [sotto-tema '{lbl}' su etichette date-locali: {len(strict)} episodi]"
        elif len(loose) >= min_n:
            eps = loose
            note = (f" [etichette date-locali davano solo {len(strict)} episodi "
                    f"(<{min_n}) → uso i sotto-temi a livello di documento]")
        else:
            note = (f" [sotto-tema '{lbl}' dava solo {len(loose)} "
                    f"episodi (<{min_n}) → uso il pool del tema]")
    if direction:
        # Match STRETTO prima (solo episodi taggati esattamente `direction`), con
        # fallback a mixed/sconosciuto solo se il pool stretto è troppo piccolo —
        # stesso pattern del filtro sotto-tema sopra. Bug corretto (2026-08-10,
        # segnalato dall'agente in sessione): la versione precedente lasciava
        # passare SEMPRE "mixed"/"" insieme a `direction`, e su temi ad alto volume
        # giornaliero (macro_data, commodity_energy — più schede/giorno tendono a
        # fondersi in "mixed" sulla chiave (data,tema)) il pool "mixed" dominava al
        # punto che --direction pos e --direction neg restituivano LO STESSO pool
        # (verificato: macro_data+nfp, 51/56 episodi "mixed" → 0 differenza pos/neg).
        # Match sulla LISTA delle direzioni osservate (vedi cmd_build): un episodio
        # conta come "pos" se almeno una delle schede di quel giorno era pos, anche
        # se un'altra era neg. Fallback alla vecchia chiave singola per librerie
        # generate prima del 2026-08-10.
        # Tre livelli, come per i sotto-temi (2026-08-19). Il livello DATE-LOCALE è
        # il solo che descriva davvero l'episodio: gli altri due dicono soltanto
        # com'era orientata la scheda che l'ha citato.
        local = [e for e in eps if direction in (e.get("directions_local") or [])]
        strict = [e for e in eps
                  if direction in (e.get("directions") or [e.get("direction", "")])]
        if len(local) >= min_n:
            eps = local
            note += (f" [direzione '{direction}' su marcatori date-locali: "
                     f"{len(local)} episodi]")
        elif len(strict) >= min_n:
            eps = strict
            note += (f" [direzione date-locale dava solo {len(local)} episodi "
                     f"(<{min_n}) → uso la direzione a livello di scheda: FILTRO DEBOLE, "
                     f"dichiaralo nel caveat]")
        else:
            eps = [e for e in eps if e["direction"] in (direction, "mixed", "")]
            note += (f" [direzione '{direction}' stretta dava solo {len(strict)} "
                     f"episodi (<{min_n}) → incluso mixed/sconosciuto]")
    dates = sorted({e["date"] for e in eps})
    # Tetto di recency: su temi a pool largo (geopolitical, commodity_energy) troppi
    # episodi diluiscono il segnale direzionale e mescolano regimi diversi. Scorecard
    # W28→W30: IC eroso proprio su quei temi e sui lunghi orizzonti, mentre macro_data
    # (pool naturalmente stretti) restava fermo. Teniamo i più RECENTI (≈ regime
    # corrente) fino a max_pool: cap che morde solo sui pool grandi, lascia intatti
    # quelli piccoli. Recency = proxy di regime, riduce il mixing a T+5/T+10.
    capped = False
    if max_pool and len(dates) > max_pool:
        dates = dates[-max_pool:]          # dates è ordinato asc → coda = più recenti
        capped = True
    print(",".join(dates))
    print(f"\n[{len(dates)} episodi · theme={theme}"
          f"{', dir='+direction if direction else ''}"
          f"{', sub='+','.join(subtheme) if subtheme else ''}"
          f"{', before '+before if before else ''}]{note}"
          f"{' [cap recency: tenuti i '+str(max_pool)+' più recenti]' if capped else ''}",
          file=__import__("sys").stderr)


def cmd_labels(theme: str | None, min_n: int):
    """Copertura delle etichette: quanti episodi porta ciascun token, per livello.

    Serve a scegliere `--subtheme` sapendo in anticipo se il filtro sarà forte
    (date-locale) o debole. Nato dall'analisi del 2026-08-16: `rate_decision`
    sembrava il token ovvio su `monetary_policy` e ne restituiva 0 date-locali,
    cosa che si scopriva solo dopo aver lanciato `find`."""
    eps = _load()
    themes = [theme] if theme else sorted({e["theme"] for e in eps})
    for th in themes:
        sub = [e for e in eps if e["theme"] == th]
        loc, doc = defaultdict(int), defaultdict(int)
        for e in sub:
            for s in e.get("subthemes_local") or []:
                loc[s] += 1
            for s in e.get("subthemes") or []:
                doc[s] += 1
        n_loc = sum(1 for e in sub if e.get("subthemes_local"))
        print(f"\n=== {th}: {len(sub)} episodi, {n_loc} con etichette date-locali")
        if not loc:
            print("    ⚠ nessuna etichetta date-locale: ogni --subtheme su questo tema "
                  "sarà un filtro DEBOLE")
        for s, n in sorted(loc.items(), key=lambda kv: -kv[1])[:15]:
            mark = "✅" if n >= min_n else "⚠ "
            print(f"  {mark} {n:4d} locali (doc {doc.get(s, 0):4d})  {s}")
        orphan = [s for s in doc if s not in loc and doc[s] >= min_n]
        if orphan:
            print(f"    solo a livello di documento (filtro debole): "
                  f"{', '.join(sorted(orphan)[:8])}")


def cmd_stats():
    eps = _load()
    by_theme = defaultdict(int)
    for e in eps:
        by_theme[e["theme"]] += 1
    for t, n in sorted(by_theme.items(), key=lambda kv: -kv[1]):
        print(f"  {n:4d}  {t}")
    print(f"  ----  totale {sum(by_theme.values())}")

    # Qualità della libreria: quanta parte è DICHIARATA dalle schede e quanta è
    # ancora dedotta con euristiche dalla prosa. È la metrica da guardare per
    # sapere se la correzione a monte del 2026-08-19 sta effettivamente entrando
    # in circolo: sale solo con le schede scritte da quella data in poi.
    n = len(eps) or 1
    decl = sum(1 for e in eps if e.get("declared"))
    nolab = sum(1 for e in eps if not e.get("subthemes_local"))
    nodir = sum(1 for e in eps if not e.get("directions_local"))
    print("\n  Qualità della libreria")
    print(f"    dichiarati dalla scheda      {decl:4d}  ({100*decl/n:4.1f}%)  ← obiettivo: in crescita")
    print(f"    senza sotto-tema date-locale {nolab:4d}  ({100*nolab/n:4.1f}%)")
    print(f"    senza direzione date-locale  {nodir:4d}  ({100*nodir/n:4.1f}%)")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    f = sub.add_parser("find")
    f.add_argument("--theme", required=True)
    f.add_argument("--direction", choices=["pos", "neg", "neutral"], default=None)
    f.add_argument("--subtheme", action="append", default=None,
                   help="Token di sotto-tema (ripetibile). Restringe il pool; "
                        "se lascia <--min-n episodi ricade sul tema.")
    f.add_argument("--min-n", type=int, default=12,
                   help="Soglia minima episodi sotto cui NON applicare il filtro sotto-tema.")
    f.add_argument("--max-pool", type=int, default=30,
                   help="Tetto di recency: se il pool supera questo numero, tiene solo gli "
                        "episodi più recenti (≈ regime corrente). Riduce diluizione e "
                        "regime-mixing sui temi larghi. 0 = nessun tetto.")
    f.add_argument("--before", default=None, metavar="YYYY-MM-DD")
    lb = sub.add_parser("labels", help="Copertura dei token di sotto-tema per livello.")
    lb.add_argument("--theme", default=None)
    lb.add_argument("--min-n", type=int, default=12,
                    help="Soglia sotto cui il token è marcato come pool magro.")
    sub.add_parser("stats")
    args = p.parse_args()
    if args.cmd == "build":
        cmd_build()
    elif args.cmd == "labels":
        cmd_labels(args.theme, args.min_n)
    elif args.cmd == "find":
        cmd_find(args.theme, args.direction, args.before, args.subtheme,
                 args.min_n, args.max_pool)
    elif args.cmd == "stats":
        cmd_stats()


if __name__ == "__main__":
    main()
