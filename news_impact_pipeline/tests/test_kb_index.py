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

# --------------------------------------------------------------------------
print("\n4. COLONNA DATA — date italiane, after close, date incerte")
# --------------------------------------------------------------------------
cd = kb_metadata.cell_date
casi_data = {
    "2016-06-23": "2016-06-23",             # ISO: presa com'è
    "7 ott 2022": "2022-10-07",             # italiana
    "**17 gen 2017**": None,                # (il grassetto lo toglie _cell, non cell_date)
    "24 mag 2023 AC": "2023-05-25",         # mercoledì AC → giovedì
    "29 set 2022 AC": "2022-09-30",         # giovedì AC → venerdì
    "30 set 2022 AC": "2022-10-03",         # venerdì AC → lunedì, non sabato
    "5 lug 2024 → ago 2024": None,          # intervallo: nessuna data puntuale
    "2006-05": None,                        # solo mese: data incerta
    "ott 2023": None,                       # solo mese: data incerta
    "31 feb 2023": None,                    # data impossibile
    "15 nov 2018 AC": "2018-11-16",
}
for cella, atteso in casi_data.items():
    check(cd(cella) == atteso, f"cell_date({cella!r}) = {cd(cella)!r}, atteso {atteso!r}")
check(cd(kb_metadata._cell("**17 gen 2017**")) == "2017-01-17", "grassetto nella cella")
print(f"   {len(casi_data) + 1} celle interpretate come atteso (AC → seduta di reazione)  ✓")


# --------------------------------------------------------------------------
# Libreria end-to-end su directory temporanee: cmd_build legge costanti di
# modulo, qui le si punta a una KB, a un archivio di schede e a un registro finti.
# --------------------------------------------------------------------------
import contextlib  # noqa: E402
import io  # noqa: E402

import analogues  # noqa: E402


def costruisci(kb_files: dict[str, str], reviews: list | None = None):
    """Esegue analogues.build su una KB temporanea; restituisce (episodi, errore)."""
    kb = kb_temporanea(kb_files)
    daily = kb / "_daily"
    daily.mkdir()
    orig = (analogues.DAILY_DIR, analogues.KB_DIR, analogues.LIB_PATH, analogues.REVIEW_PATH)
    analogues.DAILY_DIR, analogues.KB_DIR = daily, kb
    analogues.LIB_PATH, analogues.REVIEW_PATH = kb / "_episodes.yaml", kb / "_reviews.yaml"
    if reviews is not None:
        analogues.REVIEW_PATH.write_text(yaml.safe_dump({"reviews": reviews}), encoding="utf-8")
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            analogues.cmd_build()
        lib = yaml.safe_load(analogues.LIB_PATH.read_text(encoding="utf-8"))["episodes"]
        return {(e["date"], e["theme"]): e for e in lib}, None
    except ValueError as exc:
        return None, str(exc)
    finally:
        (analogues.DAILY_DIR, analogues.KB_DIR,
         analogues.LIB_PATH, analogues.REVIEW_PATH) = orig


def find_su(lib_path: Path, theme, direction, ref):
    orig = analogues.LIB_PATH
    analogues.LIB_PATH = lib_path
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            analogues.cmd_find(theme, direction, None, None, 1, 0, direction_reference=ref)
        return [d for d in buf.getvalue().strip().split(",") if d]
    finally:
        analogues.LIB_PATH = orig


# --------------------------------------------------------------------------
print("\n5. ETICHETTE DELLA SINGOLA RIGA — il caso Tankan")
# --------------------------------------------------------------------------
# La stessa data è l'episodio di una riga di tabella E il confine di una fase di
# regime nel testo. Prima le etichette arrivavano da entrambi: il Tankan prendeva
# `inflation_print` da un paragrafo che parla di CPI e di un regime successivo.
tankan = studio(subs="[tankan, cpi]", corpo=(
    "| Data (ISO) | Evento | Tipo |\n|---|---|---|\n"
    "| 2024-04-01 | Tankan Q1: grandi manifatturieri +11 | indagine Tankan |\n\n"
    "- **`post_ycc` (2024-04-01 → presente).** Rialzi dei tassi, CPI core sopra il 2%, "
    "inflazione persistente.\n"))
lib, err = costruisci({"giappone/s.md": tankan})
check(err is None, f"build fallito: {err}")
loc = set(lib[("2024-04-01", "macro_data")]["subthemes_local"])
check("tankan" in loc, f"l'etichetta della riga deve restare: {loc}")
check("inflation_print" not in loc, f"inflation_print arriva dal paragrafo di regime: {loc}")
check("cpi" not in loc, f"anche il sotto-tema dichiarato 'cpi' viene dal paragrafo: {loc}")
print(f"   2024-04-01 → {sorted(loc)}  (niente inflation_print)  ✓")

# Una data italiana della colonna Data diventa episodio, con le etichette della riga.
semis = studio(theme="structural_themes", corpo=(
    "| # | Data evento | Catalizzatore |\n|---|---|---|\n"
    "| 4 | 24 mag 2023 AC | NVDA guidance Q2: domanda AI e capex dei data center |\n"))
lib, err = costruisci({"semis/s.md": semis})
check(err is None and ("2023-05-25", "structural_themes") in lib,
      f"la data italiana AC deve diventare la seduta di reazione: {err or sorted(lib)}")
print("   «24 mag 2023 AC» → episodio 2023-05-25                   ✓")

# --------------------------------------------------------------------------
print("\n6. TABELLA CANONICA — direzioni per asset, prosa spenta")
# --------------------------------------------------------------------------
canonica = studio(theme="monetary_policy", corpo=(
    "Nota tecnica: la scorecard del 2026-09-12 lo conferma.\n\n"
    "| Data | Asset | Verso | Meccanismo | Evento | Note |\n|---|---|---|---|---|---|\n"
    "| `2024-08-05` | `^VIX` | pos | carry_unwind | unwind del carry sullo yen | |\n"
    "| `2024-08-05` | `JPY=X` | neg | carry_unwind | lo yen si rafforza | |\n"
    "| `2016-06-24` | `EURUSD=X` | pos, neg | risk_off | Brexit: euro ambiguo | |\n"))
lib, err = costruisci({"boj/s.md": canonica})
check(err is None, f"build fallito: {err}")
ep = lib[("2024-08-05", "monetary_policy")]
check(ep["directions_by_reference"] == {"^VIX": ["pos"], "JPY=X": ["neg"]},
      f"una riga = una coppia (data, asset): {ep.get('directions_by_reference')}")
check("carry_unwind" in ep["subthemes_local"], "il meccanismo della riga è un'etichetta locale")
check(ep["declared"] is True, "la riga canonica è una dichiarazione")
# La prosa è spenta: la data della nota tecnica NON diventa un episodio (R03).
check(("2026-09-12", "monetary_policy") not in lib,
      "con la tabella canonica la data di una nota tecnica non deve diventare episodio")
lib_path = kb_temporanea({}) / "lib.yaml"
lib_path.write_text(yaml.safe_dump({"episodes": list(lib.values())}), encoding="utf-8")
check(find_su(lib_path, "monetary_policy", "neg", "JPY=X") == ["2024-08-05"], "find su JPY=X neg")
check(find_su(lib_path, "monetary_policy", "pos", "^VIX") == ["2024-08-05"], "find su ^VIX pos")
check(find_su(lib_path, "monetary_policy", "pos", "JPY=X") == [], "il verso non si trasferisce fra asset")
check(find_su(lib_path, "monetary_policy", "pos", "EURUSD=X") == [] and
      find_su(lib_path, "monetary_policy", "neg", "EURUSD=X") == [],
      "`pos, neg` dichiara l'ambiguità: fuori da entrambi i pool")
print("   una riga per coppia (data, asset) → directions_by_reference  ✓")
print("   `pos, neg` escluso da entrambi i pool                        ✓")
print("   data in nota tecnica non diventa episodio (prosa spenta)     ✓")

# Validazione della tabella canonica: ogni campo sbagliato è un ERRORE.
_, dichiarate = kb_metadata.kb_tables(kb_metadata.strip(studio(corpo=(
    "| Data | Asset | Verso | Meccanismo | Evento |\n|---|---|---|---|---|\n"
    "| 5 ago 2024 | ^VIX | pos | carry_unwind | data non ISO |\n"
    "| 2024-08-05 | JGB | pos | carry_unwind | ticker non in DB |\n"
    "| 2024-08-05 | ^VIX | rialzo | carry_unwind | verso fuori vocabolario |\n"
    "| 2024-08-05 | ^VIX | pos |  | meccanismo vuoto |\n"
    "| 2024-08-05 | ^VIX | pos, neg | carry_unwind | ambiguo ma VALIDO |\n"))))
errs = kb_metadata.errors(kb_metadata.validate_declared(dichiarate, {"^VIX"}))
check(len(errs) == 4, f"attesi 4 errori, uno per riga rotta: {errs}")
print("   righe canoniche malformate → 4 errori, `pos, neg` valido     ✓")

# --------------------------------------------------------------------------
print("\n7. REGISTRO — revisioni con fonte research")
# --------------------------------------------------------------------------
legacy = studio(theme="geopolitical", corpo=(
    "| Data (ISO) | Evento | Direzione attesa | Asset-canale |\n|---|---|---|---|\n"
    "| 2016-06-23 | Referendum Brexit | GBP ↑ se Remain (atteso) | GBPUSD=X |\n"))
rev = {"date": "2016-06-23", "theme": "geopolitical", "reference": "GBPUSD=X",
       "source": "uk/s.md", "reason": "Il mercato prezzava Remain alla chiusura.",
       "direction": "pos"}

lib, err = costruisci({"uk/s.md": legacy}, [{**rev, "source": "kb:uk/s.md",
                                             "mechanism": ["referendum"],
                                             "description": "Referendum Brexit, voto"}])
check(err is None, f"una revisione con fonte research deve essere ammessa: {err}")
ep = lib[("2016-06-23", "geopolitical")]
check(ep["directions_by_reference"] == {"GBPUSD=X": ["pos"]}, "direzione dalla revisione")
check(ep["direction_sources"] == {"GBPUSD=X": ["kb:uk/s.md"]}, "provenienza tracciata")
check("referendum" in ep["subthemes_local"], "il mechanism della revisione è un'etichetta locale")
print("   fonte kb: ammessa, provenienza e meccanismo registrati        ✓")

_, err = costruisci({"uk/s.md": legacy}, [{**rev, "source": "kb:uk/s.md",
                                           "date": "2016-06-24"}])
check(err is not None, "una revisione su una data che la research non contiene va rifiutata")
_, err = costruisci({"uk/s.md": legacy}, [{**rev, "source": "kb:uk/inesistente.md"}])
check(err is not None, "una revisione con fonte KB inesistente va rifiutata")
_, err = costruisci({"uk/s.md": legacy}, [{**rev, "source": "kb:uk/s.md",
                                           "description": ["non", "testo"]}])
check(err is not None, "description deve essere testo")
print("   data assente, fonte inesistente, campi malformati → rifiutati ✓")

# Le righe compilate a mano prima del 2026-09-23 non hanno mechanism/description
# e non devono diventare invalide.
lib, err = costruisci({"uk/s.md": legacy}, [{**rev, "source": "kb:uk/s.md"}])
check(err is None, f"una revisione senza i campi nuovi deve restare valida: {err}")
print("   revisione senza mechanism/description → ancora valida         ✓")

print("\n" + "=" * 78)
print(f"ASSERZIONI: {OK}   ·   FALLITE: 0")
print("=" * 78)
print("Tutte verdi.")
