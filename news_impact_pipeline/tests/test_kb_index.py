#!/usr/bin/env python3
"""
test_kb_index.py — il parser unico dei metadati KB e lo scanner dell'indice.

Non distruttivo: ogni caso lavora su una KB temporanea, mai sui file reali.

Copre i tre difetti che il Run 5b chiude (R04):
  1. due parser divergenti sullo stesso YAML valido (tema perso, liste perse);
  2. un errore di schema che pubblicava comunque un catalogo degradato;
  3. uno scanner con una PROPRIA nozione di «indicizzato», cieco a rimozioni,
     rinomine, profondità e secondo studio nella stessa cartella.
"""

import sys
import tempfile
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import build_catalog  # noqa: E402
import kb_metadata  # noqa: E402

OK = 0


def check(cond, msg):
    global OK
    assert cond, f"FALLITO: {msg}"
    OK += 1


META = """```yaml
title: "Studio"
date_compiled: 2026-01-01
primary_theme: {theme}
sub_themes: {subs}
relevant_assets: [^GSPC]
external_assets_mentioned: nessuno
time_window:
  start: 2020-01-01
  end: present
regime_phases:
  - fase_uno: 2020-01-01 to present
keywords: [a, b]
```
"""


def studio(theme='macro_data', subs='[cpi, inflation]', corpo='episodio `2020-03-09`'):
    return f"# Studio\n\n{corpo}\n\n" + META.format(theme=theme, subs=subs)


def kb_temporanea(files: dict[str, str]) -> Path:
    """files: {'cartella/file.md': contenuto}. Restituisce la root."""
    root = Path(tempfile.mkdtemp(prefix="kbtest_"))
    for rel, testo in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(testo, encoding="utf-8")
    return root


def scan_su(kb: Path, catalogo: Path) -> tuple[bool, list[str]]:
    """Esegue scan() su una KB temporanea e ne legge l'output."""
    import io
    import contextlib
    orig_kb, orig_cat = build_catalog.KB_DIR, build_catalog.CATALOG_PATH
    build_catalog.KB_DIR, build_catalog.CATALOG_PATH = kb, catalogo
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            build_catalog.scan()
    finally:
        build_catalog.KB_DIR, build_catalog.CATALOG_PATH = orig_kb, orig_cat
    righe = buf.getvalue().splitlines()
    stale = "STALE=1" in righe
    return stale, sorted(r.split("=", 1)[1] for r in righe if r.startswith("UNINDEXED="))


def scrivi_catalogo(kb: Path, rels: list[str]) -> Path:
    """Un catalogo che indicizza esattamente `rels`, più vecchio dei sorgenti."""
    cat = kb / "catalog.yaml"
    cat.write_text(yaml.safe_dump(
        {"generated_at": "2026-01-01T00:00:00", "num_entries": len(rels),
         "entries": [{"source_file": r} for r in rels]}), encoding="utf-8")
    # il catalogo deve risultare PIU' RECENTE dei sorgenti, altrimenti lo
    # staleness per mtime scatta sempre e i casi non sarebbero distinguibili
    import os
    import time
    dopo = time.time() + 10
    os.utime(cat, (dopo, dopo))
    return cat


print("=" * 78)
print("SESSIONE DI TEST — kb_metadata + scanner dell'indice")
print("=" * 78)

# --------------------------------------------------------------------------
print("\n1. UN SOLO PARSER — il quoting non deve cambiare il risultato")
# --------------------------------------------------------------------------
# Il difetto storico: harvest_kb leggeva il testo grezzo con regex proprie, e
# su YAML valido dava un risultato DIVERSO dal catalogo. Tema vuoto = tutti gli
# episodi della research scartati da cmd_build, in silenzio.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from analogues import harvest_kb  # noqa: E402

for etichetta, theme, subs in [
    ("non quotato", "macro_data", "[cpi, inflation]"),
    ("quotato doppio", '"macro_data"', '["cpi", "inflation"]'),
    ("quotato singolo", "'macro_data'", "['cpi', 'inflation']"),
    ("lista multilinea", "macro_data", "\n  - cpi\n  - inflation"),
]:
    kb = kb_temporanea({"studio/s.md": studio(theme=theme, subs=subs)})
    t, st, dates, body = harvest_kb(kb / "studio" / "s.md")
    check(t == "macro_data", f"{etichetta}: tema '{t}' invece di macro_data")
    check(st == {"cpi", "inflation"}, f"{etichetta}: sub_themes {st}")
    check("2020-03-09" in dates, f"{etichetta}: episodio in prosa perso")
    print(f"   {etichetta:18s} tema={t!r} sub={sorted(st)}  ✓")

# Il blocco di metadata non deve contribuire date: i suoi confini di regime
# erano finiti in libreria come episodi fasulli (67 al 2026-08-15).
kb = kb_temporanea({"studio/s.md": studio()})
_, _, dates, body = harvest_kb(kb / "studio" / "s.md")
check("2020-01-01" not in dates, "un confine di regime è diventato un episodio")
check("```yaml" not in body, "il blocco metadata è rimasto nel corpo")
print("   confini di regime esclusi dagli episodi                  ✓")

# --------------------------------------------------------------------------
print("\n2. SCHEMA — un tipo sbagliato è un ERRORE, non un avviso")
# --------------------------------------------------------------------------
tick = {"^GSPC"}
base = kb_metadata.extract(studio())
check(kb_metadata.errors(kb_metadata.validate(base, tick)) == [], "lo studio valido deve passare")

# Il caso reale: la research BoJ scriveva entrambi i campi a stringa, passava la
# validazione, e monthly_digest.kb_regimes restituiva ')' come fase corrente —
# perché su una stringa phases[-1] è l'ultimo CARATTERE.
rotti = {
    "time_window a stringa": {"time_window": "start 1998-01-01, end present"},
    "regime_phases a stringa": {"regime_phases": "fase (1998-01-01 to 2012-12-31)"},
    "intervallo non canonico": {"regime_phases": [{"a": "1998/01/01 - 2012/12/31"}]},
    "fase a due chiavi": {"regime_phases": [{"a": "2020-01-01 to present", "b": "x"}]},
    "tema fuori ontologia": {"primary_theme": "inventato"},
    "tema annotato": {"primary_theme": "macro_data (sub: usa)"},
    "sub_themes a stringa": {"sub_themes": "cpi, inflation"},
    "data quotata": {"date_compiled": "2026-01-01"},
    "data futura": {"date_compiled": date(2099, 1, 1)},
    "campo mancante": {k: v for k, v in base.items() if k != "keywords"},
}
for etichetta, patch in rotti.items():
    meta = patch if etichetta == "campo mancante" else {**base, **patch}
    errs = kb_metadata.errors(kb_metadata.validate(meta, tick))
    check(errs, f"'{etichetta}' doveva produrre un ERRORE")
    print(f"   {etichetta:24s} → errore  ✓")

# Un ticker esterno NON blocca: esiste external_assets_mentioned per dichiararlo.
f = kb_metadata.validate({**base, "relevant_assets": ["^GSPC", "JGB"]}, tick)
check(kb_metadata.errors(f) == [], "un ticker esterno non deve bloccare")
check(any(l == kb_metadata.WARN for l, _ in f), "un ticker esterno deve avvisare")
print("   ticker esterno           → avviso, non errore  ✓")

# --------------------------------------------------------------------------
print("\n3. SCANNER — rimozioni, rinomine, profondità, secondo studio")
# --------------------------------------------------------------------------
# 3.1 stato allineato
kb = kb_temporanea({"a/s.md": studio(), "b/s.md": studio()})
cat = scrivi_catalogo(kb, ["a/s.md", "b/s.md"])
stale, unind = scan_su(kb, cat)
check(not stale and unind == [], f"stato allineato: stale={stale} unind={unind}")
print("   catalogo allineato                     → STALE=0  ✓")

# 3.2 RIMOZIONE — il difetto principale: per sola mtime non si vedeva mai
cat = scrivi_catalogo(kb, ["a/s.md", "b/s.md", "sparita/s.md"])
stale, _ = scan_su(kb, cat)
check(stale, "una research rimossa dal disco deve rendere stale il catalogo")
print("   research rimossa dal disco             → STALE=1  ✓")

# 3.3 RINOMINA — stesso numero di voci, nomi diversi
cat = scrivi_catalogo(kb, ["a/s.md", "b/vecchio_nome.md"])
stale, _ = scan_su(kb, cat)
check(stale, "una rinomina deve rendere stale il catalogo")
print("   research rinominata                    → STALE=1  ✓")

# 3.4 AGGIUNTA
cat = scrivi_catalogo(kb, ["a/s.md"])
stale, _ = scan_su(kb, cat)
check(stale, "una research nuova deve rendere stale il catalogo")
print("   research aggiunta                      → STALE=1  ✓")

# 3.5 PROFONDITA' — il builder è ricorsivo, lo scanner shell non lo era
kb = kb_temporanea({"a/sotto/piu/giu.md": studio()})
cat = scrivi_catalogo(kb, [])
stale, _ = scan_su(kb, cat)
check(stale, "uno studio annidato in profondità deve essere visto")
print("   studio annidato in profondità          → STALE=1  ✓")

# 3.6 SECONDO STUDIO nella stessa cartella: lo shell marcava l'INTERA cartella
#     indicizzata se un qualsiasi .md aveva un fence, e il secondo spariva.
kb = kb_temporanea({"a/con_meta.md": studio(),
                    "a/senza_meta.md": "# Studio grezzo\n\nsolo prosa, nessun blocco\n"})
cat = scrivi_catalogo(kb, ["a/con_meta.md"])
stale, unind = scan_su(kb, cat)
check(not stale, "il file senza blocco non deve rendere stale il catalogo")
check(unind == [], "una cartella con almeno uno studio indicizzato non è 'da indicizzare'")
print("   cartella mista (uno sì, uno no)        → coerente  ✓")

# 3.7 cartella SENZA alcun blocco leggibile → da indicizzare
kb = kb_temporanea({"nuova/grezzo.md": "# Solo prosa\n", "a/s.md": studio()})
cat = scrivi_catalogo(kb, ["a/s.md"])
stale, unind = scan_su(kb, cat)
check(unind == ["nuova"], f"la cartella senza metadati doveva risultare da indicizzare: {unind}")
print("   cartella senza metadati                → UNINDEXED  ✓")

# 3.8 il prefisso '_' resta escluso: i prompt contengono un ```yaml di esempio
kb = kb_temporanea({"a/s.md": studio(), "_prompts/tpl.md": studio()})
cat = scrivi_catalogo(kb, ["a/s.md"])
stale, unind = scan_su(kb, cat)
check(not stale and unind == [], "i percorsi con prefisso _ non sono studi")
print("   _prompts ignorato                      → coerente  ✓")

print("\n" + "=" * 78)
print(f"ASSERZIONI: {OK}   ·   FALLITE: 0")
print("=" * 78)
print("Tutte verdi.")
