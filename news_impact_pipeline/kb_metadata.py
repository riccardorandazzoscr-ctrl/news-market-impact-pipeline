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
from datetime import date, datetime

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
