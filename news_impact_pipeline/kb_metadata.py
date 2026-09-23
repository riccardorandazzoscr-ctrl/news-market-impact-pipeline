#!/usr/bin/env python3
"""
kb_metadata.py — l'UNICO parser dei metadati delle research KB.

Prima esistevano due letture divergenti dello stesso blocco YAML: `build_catalog`
lo caricava con `yaml.safe_load`, `analogues.harvest_kb` lo rileggeva con regex
proprie (`primary_theme:\\s*([^\\n]+)`, `sub_themes:\\s*\\[([^\\]]*)\\]`). Su YAML
valido i due risultati differivano, e la differenza era silenziosa:

    primary_theme: "macro_data"   → catalogo 'macro_data' · estrattore ''
    primary_theme: 'macro_data'   → catalogo 'macro_data' · estrattore ''
    sub_themes:                   → catalogo [cpi, inflation] · estrattore []
      - cpi

Un tema vuoto fa scartare la riga da `analogues.cmd_build`, quindi una research
con il tema fra virgolette appariva perfetta nel catalogo e contribuiva ZERO
episodi alla libreria. Qui il blocco si legge una volta sola, con YAML.

Lo schema validato (§5.1 della spec 2026-09-21-r04-r01) distingue errori da
avvisi: un ERRORE non deve pubblicare un indice degradato, un avviso sì.

Nessuna dipendenza pesante: questo modulo lo importano sia il builder sia
l'estrattore, e `analogues.py` non deve pagare pandas/yfinance per leggere un
blocco YAML (stessa ragione per cui esiste `diagnosi_serie.py`).
"""

import re
from datetime import date, datetime, timedelta

import yaml

# Ontologia delle notizie (Design Document §6.1).
ONTOLOGY = {
    "monetary_policy", "fiscal_policy", "geopolitical", "macro_data",
    "corporate_idiosyncratic", "regulatory", "commodity_energy",
    "financial_stability", "structural_themes",
}

REQUIRED_FIELDS = ("title", "date_compiled", "primary_theme", "sub_themes",
                   "relevant_assets", "time_window", "regime_phases", "keywords")

LIST_FIELDS = ("sub_themes", "relevant_assets", "keywords")

# Blocco di metadata in coda alla research: ```yaml ... ```
_FENCED_RE = re.compile(r"```yaml\s*\n(.*?)\n```", re.S)
# Fallback storico: un blocco --- ... --- in fondo al file.
_DASHED_RE = re.compile(r"\n---\s*\n(.*?)\n---\s*(?:\n|$)", re.S)
# Per ripulire il CORPO: il blocco contiene date che non sono episodi
# (`date_compiled`, estremi di `time_window` e `regime_phases`).
_STRIP_RE = re.compile(r"\n```yaml\b.*?(?:\n```|\Z)", re.S)

_PHASE_RANGE_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}\s+to\s+(\d{4}-\d{2}-\d{2}|present)$")

ERROR, WARN = "ERRORE", "avviso"


def extract(md_text: str) -> dict | None:
    """Il blocco di metadata in coda al markdown, o None se assente/illeggibile.

    Convenzione: «il blocco metadata sta in fondo» → si prende l'ULTIMO."""
    blocks = _FENCED_RE.findall(md_text)
    if blocks:
        raw = re.sub(r"\n---\s*$", "", re.sub(r"^---\s*\n", "", blocks[-1].strip()))
    else:
        m = list(_DASHED_RE.finditer(md_text))
        if not m:
            return None
        raw = m[-1].group(1).strip()
    try:
        meta = yaml.safe_load(raw)
    except yaml.YAMLError:
        return None
    return meta if isinstance(meta, dict) else None


def strip(md_text: str) -> str:
    """Il corpo senza i blocchi di metadata: quel che resta sono episodi in prosa."""
    return _STRIP_RE.sub("\n", md_text)


def is_study(rel_parts) -> bool:
    """Un percorso relativo alla KB è uno studio indicizzabile?

    Convenzione «_ = non indicizzare»: tiene fuori `_prompts/` (che contiene
    blocchi YAML di esempio) e gli indici generati (`_episodes.yaml`). Vive qui
    perché scanner e builder devono usare la STESSA regola di scoperta."""
    return not any(p.startswith("_") for p in rel_parts)


def iter_studies(kb_dir):
    """I markdown di studio sotto `kb_dir`, ricorsivo e ordinato."""
    return sorted(f for f in kb_dir.rglob("*.md")
                  if is_study(f.relative_to(kb_dir).parts))


def _is_str_list(v) -> bool:
    return isinstance(v, list) and all(isinstance(x, str) for x in v)


def validate(meta: dict, known_tickers: set[str]) -> list[tuple[str, str]]:
    """Controlla i metadati. Restituisce [(livello, messaggio)].

    Un ERRORE significa «non pubblicare»: il dato è di un tipo su cui i consumatori
    a valle sbagliano in silenzio. Un avviso è informativo."""
    out: list[tuple[str, str]] = []

    for f in REQUIRED_FIELDS:
        if f not in meta:
            out.append((ERROR, f"campo mancante: '{f}'"))

    if "title" in meta and not (isinstance(meta["title"], str) and meta["title"].strip()):
        out.append((ERROR, "title deve essere una stringa non vuota"))

    dc = meta.get("date_compiled")
    if dc is not None:
        if not isinstance(dc, (date, datetime)):
            out.append((ERROR, f"date_compiled {dc!r} non è una data YAML "
                               f"(attesa YYYY-MM-DD senza virgolette)"))
        else:
            d = dc.date() if isinstance(dc, datetime) else dc
            if d > date.today():
                out.append((ERROR, f"date_compiled {d} è nel futuro"))

    pt = meta.get("primary_theme")
    if pt is not None and pt not in ONTOLOGY:
        out.append((ERROR, f"primary_theme {pt!r} non è nell'ontologia §6.1 "
                           f"(ammessi: {sorted(ONTOLOGY)})"))

    for f in LIST_FIELDS:
        if f in meta and not _is_str_list(meta[f]):
            out.append((ERROR, f"{f} deve essere una lista di stringhe, "
                               f"trovato {type(meta[f]).__name__}"))

    # time_window e regime_phases sono i due campi che passavano come stringa.
    # `monthly_digest.kb_regimes` fa `phases[-1]`: su una stringa l'ultimo
    # elemento è l'ultimo CARATTERE, ed è così che la fase corrente della
    # research BoJ risultava ')'. Tipizzare qui chiude il bug alla radice.
    tw = meta.get("time_window")
    if tw is not None:
        if not isinstance(tw, dict):
            out.append((ERROR, f"time_window deve essere una mappa "
                               f"{{start, end}}, trovato {type(tw).__name__}"))
        elif set(tw) != {"start", "end"}:
            out.append((ERROR, f"time_window deve avere esattamente le chiavi "
                               f"start ed end, trovato {sorted(tw)}"))

    rp = meta.get("regime_phases")
    if rp is not None:
        if not isinstance(rp, list):
            out.append((ERROR, f"regime_phases deve essere una lista di fasi, "
                               f"trovato {type(rp).__name__}"))
        else:
            for i, ph in enumerate(rp):
                if not isinstance(ph, dict) or len(ph) != 1:
                    out.append((ERROR, f"regime_phases[{i}] deve essere una mappa "
                                       f"a chiave singola {{nome: intervallo}}"))
                    continue
                (nome, intervallo), = ph.items()
                if not isinstance(intervallo, str) or not _PHASE_RANGE_RE.match(intervallo):
                    out.append((ERROR, f"regime_phases[{i}] '{nome}': intervallo "
                                       f"{intervallo!r} non è 'YYYY-MM-DD to "
                                       f"(YYYY-MM-DD|present)'"))

    # Un ticker esterno è legittimo: esiste `external_assets_mentioned` per
    # dichiararlo. Resta un avviso, non blocca la pubblicazione.
    assets = meta.get("relevant_assets")
    if _is_str_list(assets):
        for a in assets:
            if a not in known_tickers:
                out.append((WARN, f"asset '{a}' non è nella tabella 'assets' del DB"))

    return out


def errors(findings) -> list[str]:
    return [m for lvl, m in findings if lvl == ERROR]


# ---------------------------------------------------------------------------
# Tabelle di episodi nel corpo della research
#
# Le research hanno quasi tutte una tabella di episodi (§3 del template), ma
# l'estrattore la ignorava: raccoglieva ogni data ISO del corpo e ne derivava le
# etichette da TUTTE le righe in cui la data compariva. Due difetti ne seguivano:
#   - il Tankan del 2024-04-01 prendeva `inflation_print` dal paragrafo sul
#     regime successivo, che condivide la data come confine di fase;
#   - la research semiconduttori scrive le date in italiano («24 mag 2023 AC») e
#     contribuiva zero episodi da una tabella di dodici eventi reali.
# Qui le tabelle si leggono per INTESTAZIONE, così la riga di un episodio è il
# suo contesto e la colonna Data si interpreta anche quando non è ISO.
# ---------------------------------------------------------------------------

_TABLE_RE = re.compile(
    r"^[ \t]*\|(.*)\|[ \t]*\n[ \t]*\|[ \t:|\-]+\|[ \t]*\n((?:[ \t]*\|.*(?:\n|$))*)", re.M)

# Tabella canonica delle research (spec 2026-09-21 §3): una riga per coppia
# (data, asset). Colonne aggiuntive in coda (es. Note) sono ammesse.
CANON_HEADER = ["data", "asset", "verso", "meccanismo", "evento"]
VERSI = {"pos", "neg", "neutral"}

_MESI = {"gen": 1, "feb": 2, "mar": 3, "apr": 4, "mag": 5, "giu": 6,
         "lug": 7, "ago": 8, "set": 9, "ott": 10, "nov": 11, "dic": 12}
_ISO_CELL_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\b")
_IT_CELL_RE = re.compile(r"^(\d{1,2})\s+([a-zà]{3})[a-zà]*\.?\s+(\d{4})\b(.*)$", re.I)


def _cell(c: str) -> str:
    return c.strip().strip("`*").strip()


def tables(text: str) -> list[tuple[list[str], list[tuple[str, list[str]]]]]:
    """Tabelle markdown: [(intestazioni minuscole, [(riga grezza, celle)])]."""
    out = []
    for m in _TABLE_RE.finditer(text):
        head = [_cell(c).lower() for c in m.group(1).split("|")]
        rows = []
        for line in m.group(2).splitlines():
            s = line.strip()
            if not s:
                continue
            s = s[1:] if s.startswith("|") else s
            s = s[:-1] if s.endswith("|") else s
            rows.append((line, [_cell(c) for c in s.split("|")]))
        out.append((head, rows))
    return out


def cell_date(cell: str) -> str | None:
    """Data della colonna Data di una tabella di episodi → ISO, o None.

    - ISO (`2016-06-23`): presa com'è — per il template è già la seduta giusta.
    - Italiana (`24 mag 2023`): convertita. Con il marcatore `AC` (after close)
      diventa il giorno feriale successivo, perché il template fissa la data
      nella **prima seduta in cui l'asset reagisce**. L'event study ancora T=0
      alla chiusura del primo giorno ≥ data: con la data dell'annuncio serale il
      T+1 conterrebbe la reazione, e l'episodio misurerebbe una cosa diversa
      dagli altri del pool (che misurano la prosecuzione). Un festivo non serve
      calcolarlo: l'event study scivola già alla seduta successiva.
    - Solo mese/anno (`2006-05`, `ott 2023`): data incerta → None. Non si indovina.
    """
    m = _ISO_CELL_RE.match(cell)
    if m:
        try:
            return date(*map(int, m.groups())).isoformat()
        except ValueError:
            return None
    m = _IT_CELL_RE.match(cell)
    if not m or m.group(2).lower()[:3] not in _MESI:
        return None
    # Un intervallo nella cella («5 lug 2024 → ago 2024») non è una data puntuale:
    # l'autore non ne ha indicata una. Regola del template: meglio una data in
    # meno che una sbagliata.
    if re.match(r"\s*(→|->|–|—|-)\s*\S", m.group(4)):
        return None
    try:
        d = date(int(m.group(3)), _MESI[m.group(2).lower()[:3]], int(m.group(1)))
    except ValueError:
        return None
    if re.search(r"\bAC\b", m.group(4)):
        d += timedelta(days=1)
        while d.weekday() >= 5:
            d += timedelta(days=1)
    return d.isoformat()


def kb_tables(body: str) -> tuple[dict[str, list[str]], list[dict]]:
    """Legge la struttura di una research.

    Restituisce:
      - {data ISO: [righe grezze]} dalle tabelle di episodi in formato libero
        (quelle con una colonna Data): la riga è il contesto dell'episodio;
      - le righe della tabella CANONICA, campi grezzi ancora da validare.
    """
    rows: dict[str, list[str]] = {}
    declared: list[dict] = []
    for head, trows in tables(body):
        if head[:5] == CANON_HEADER:
            for line, c in trows:
                if len(c) >= 5:
                    declared.append({"date": c[0], "asset": c[1], "verso": c[2],
                                     "mechanism": c[3], "event": c[4], "line": line})
            continue
        idx = next((i for i, h in enumerate(head)
                    if h.startswith("data") or h == "date"), None)
        if idx is None:
            continue
        for line, c in trows:
            if idx < len(c) and (d := cell_date(c[idx])):
                rows.setdefault(d, []).append(line)
    return rows, declared


def declared_versi(raw: str) -> set[str] | None:
    """Verso di una riga canonica → insieme di token, o None se illeggibile.
    `pos, neg` è un verso VALIDO: dichiara l'ambiguità ed esclude la riga dai pool."""
    versi = {v.strip().lower() for v in re.split(r"[,/]", raw or "") if v.strip()}
    return versi if versi and versi <= VERSI else None


def validate_declared(declared: list[dict], known_tickers: set[str]) -> list[tuple[str, str]]:
    """Righe della tabella canonica: ogni campo è un ERRORE se non valido.

    Una dichiarazione su un ticker inesistente non produrrà mai un event study,
    e una data non ISO nella tabella canonica rompe il contratto: meglio fermare
    la pubblicazione che ammettere una riga che il filtro scarterebbe in silenzio."""
    out = []
    oggi = date.today().isoformat()
    for r in declared:
        where = f"tabella episodi, riga '{r['date']} | {r['asset']}'"
        m = _ISO_CELL_RE.match(r["date"])
        if not m or r["date"] != m.group(0) or not cell_date(r["date"]):
            out.append((ERROR, f"{where}: data non ISO YYYY-MM-DD"))
        elif r["date"] > oggi:
            out.append((ERROR, f"{where}: data futura"))
        if r["asset"] not in known_tickers:
            out.append((ERROR, f"{where}: asset '{r['asset']}' non è nella tabella 'assets'"))
        if declared_versi(r["verso"]) is None:
            out.append((ERROR, f"{where}: verso '{r['verso']}' non è pos/neg/neutral"))
        if not r["mechanism"].strip():
            out.append((ERROR, f"{where}: meccanismo vuoto"))
    return out


def _self_check():
    """Check runnabile: `python kb_metadata.py`. Niente framework, niente fixture."""
    tick = {"^GSPC", "JPY=X"}
    base = {"title": "X", "date_compiled": date(2026, 1, 1),
            "primary_theme": "macro_data", "sub_themes": ["cpi"],
            "relevant_assets": ["^GSPC"], "keywords": ["a"],
            "time_window": {"start": "2020-01-01", "end": "present"},
            "regime_phases": [{"fase_uno": "2020-01-01 to present"}]}
    assert validate(base, tick) == [], validate(base, tick)

    # Il quoting non deve più cambiare il risultato: è il difetto che questo
    # modulo esiste per chiudere.
    doc = ('# S\n\nepisodio `2020-03-09`\n\n```yaml\ntitle: "X"\n'
           'primary_theme: "macro_data"\nsub_themes:\n  - cpi\n  - inflation\n```\n')
    meta = extract(doc)
    assert meta["primary_theme"] == "macro_data", meta
    assert meta["sub_themes"] == ["cpi", "inflation"], meta
    assert "```yaml" not in strip(doc) and "2020-03-09" in strip(doc)

    def err(**kw):
        return errors(validate({**base, **kw}, tick))

    assert err(time_window="start 1998-01-01, end present"), "stringa deve fallire"
    assert err(regime_phases="fase (1998-01-01 to 2012-12-31)"), "stringa deve fallire"
    assert err(regime_phases=[{"a": "1998-01-01 - 2012-12-31"}]), "separatore errato"
    assert err(regime_phases=[{"a": "1998-01-01 to 2012-12-31", "b": "x"}]), "due chiavi"
    assert err(primary_theme="macro_data (sub: usa)"), "tema annotato non è canonico"
    assert err(sub_themes="cpi, inflation"), "stringa al posto di lista"
    assert err(date_compiled="2026-01-01"), "data quotata è una stringa"
    assert err(date_compiled=date(2099, 1, 1)), "data futura"
    assert err(time_window={"start": "2020-01-01"}), "chiave mancante"
    assert not err(regime_phases=[{"a": "1998-01-01 to 2012-12-31"},
                                  {"b": "2013-01-01 to present"}])
    # Ticker esterno: avviso, non errore — blocca la pubblicazione sarebbe sbagliato.
    f = validate({**base, "relevant_assets": ["^GSPC", "JGB"]}, tick)
    assert errors(f) == [] and any(lvl == WARN for lvl, _ in f), f

    assert extract("nessun blocco") is None
    assert extract("```yaml\n: : non valido :\n```") is None
    assert is_study(("studio", "a.md")) and not is_study(("_prompts", "a.md"))
    print("kb_metadata: tutti i check passati")


if __name__ == "__main__":
    _self_check()
