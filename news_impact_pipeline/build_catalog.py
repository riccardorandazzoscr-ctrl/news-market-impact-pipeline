#!/usr/bin/env python3
"""
build_catalog.py

Rigenera catalog.yaml scansionando tutti i file markdown della Knowledge Base.

Per ogni .md in ~/Claude/knowledge_base/ estrae il blocco YAML di metadata
posto alla fine del file (dentro un fenced block ```yaml ... ``` oppure come
blocco --- ... --- diretto), valida i campi contro:
  - l'ontologia delle notizie (Design_Document §6.1)
  - i ticker presenti nel database asset

Produce:
  - knowledge_base/catalog.yaml  (indice aggregato consultabile dal sistema)
  - un report a video con eventuali warning di validazione

Come si usa:
    venv/bin/python build_catalog.py
"""

import os
import sqlite3
from datetime import datetime
from pathlib import Path

import yaml

import kb_metadata
from diagnosi_serie import DB_PATH


KB_DIR = Path.home() / "Claude" / "mercati_finanza" / "knowledge_base"
CATALOG_PATH = KB_DIR / "catalog.yaml"


def get_known_tickers(conn) -> set[str]:
    """Legge dal DB l'elenco dei ticker registrati nella tabella assets."""
    rows = conn.execute("SELECT ticker FROM assets").fetchall()
    return {r[0] for r in rows}


def scan():
    """Risponde allo scanner: cosa manca all'indice e se il catalogo è stale.

    Esiste perché `index_studies.sh` aveva una PROPRIA nozione di «indicizzato»
    che divergeva dal builder su tre punti: marcava indicizzata un'intera
    cartella se un qualsiasi .md conteneva un fence ```yaml (anche invalido, e
    anche se un secondo studio nella stessa cartella non ne aveva); cercava a un
    solo livello di profondità mentre il builder è ricorsivo; e rilevava lo
    staleness per sola mtime, quindi una research RIMOSSA o RINOMINATA lasciava
    la sua voce nel catalogo per sempre.

    Qui la domanda la risponde chi possiede la regola. Output per lo shell:
        STALE=0|1
        UNINDEXED=<nome cartella>
    """
    studies = kb_metadata.iter_studies(KB_DIR)
    con_meta = {str(f.relative_to(KB_DIR)) for f in studies
                if kb_metadata.extract(f.read_text(encoding="utf-8")) is not None}

    # Cartelle di primo livello che hanno materiale .md ma nessun blocco leggibile.
    cartelle = {}
    for f in studies:
        cartelle.setdefault(f.relative_to(KB_DIR).parts[0], []).append(
            str(f.relative_to(KB_DIR)))
    non_indicizzate = sorted(nome for nome, rels in cartelle.items()
                             if not any(r in con_meta for r in rels))

    # Staleness per CONTENUTO (cattura aggiunte, rimozioni e rinomine) più mtime
    # (cattura le modifiche a un file già indicizzato).
    if not CATALOG_PATH.exists():
        stale = True
    else:
        catalogo = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8")) or {}
        indicizzati = {e.get("source_file") for e in catalogo.get("entries", [])}
        stale = indicizzati != con_meta or any(
            (KB_DIR / r).stat().st_mtime > CATALOG_PATH.stat().st_mtime
            for r in con_meta)

    print(f"STALE={int(stale)}")
    for nome in non_indicizzate:
        print(f"UNINDEXED={nome}")


def main():
    if not KB_DIR.exists():
        raise SystemExit(f"Cartella Knowledge Base non trovata: {KB_DIR}")

    # Scoperta condivisa con l'estrattore della libreria: la regola «_ = non
    # indicizzare» vive in kb_metadata, così scanner e builder non possono
    # divergere su QUALI file sono studi.
    md_files = kb_metadata.iter_studies(KB_DIR)
    if not md_files:
        print(f"Nessun file .md trovato in {KB_DIR}")
        return

    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        known_tickers = get_known_tickers(conn)
    finally:
        conn.close()

    print(f"=== Costruzione catalog.yaml ===")
    print(f"Scansione di {KB_DIR}")
    print(f"Asset registrati nel DB: {len(known_tickers)}\n")

    entries = []
    n_warn = 0
    failed: list[tuple[str, list[str]]] = []

    for f in md_files:
        rel = str(f.relative_to(KB_DIR))  # es. "sovereign_debt/sovereign_debt_crisis.md"
        text = f.read_text(encoding="utf-8")
        meta = kb_metadata.extract(text)

        if meta is None:
            # File senza blocco (PDF riesportati, note, raw export): non è uno
            # studio, non è un errore.
            print(f"  [SKIP]  {rel}: nessun blocco YAML trovato")
            continue

        # Metadati e, se la research la usa, la tabella canonica degli episodi:
        # un ticker inesistente o un verso fuori vocabolario sono errori, perché
        # la libreria scarterebbe quella riga senza dirlo a nessuno.
        _, declared = kb_metadata.kb_tables(kb_metadata.strip(text))
        findings = (kb_metadata.validate(meta, known_tickers)
                    + kb_metadata.validate_declared(declared, known_tickers))
        errs = kb_metadata.errors(findings)
        for lvl, msg in findings:
            print(f"  [{lvl:7s}] {rel}: {msg}")
        if errs:
            failed.append((rel, errs))
        else:
            n_warn += len(findings)
            if not findings:
                print(f"  [OK]     {rel}")

        # Path relativo alla KB come riferimento sorgente (tracciabilita').
        entries.append({"source_file": rel, **meta})

    # Un errore NON pubblica. Prima un catalogo degradato veniva scritto lo
    # stesso e i consumatori a valle ci sbattevano contro molto più tardi:
    # `monthly_digest.kb_regimes` leggeva ')' come fase corrente da un
    # regime_phases scritto a stringa, senza che nulla avesse segnalato niente.
    if failed:
        print(f"\n--- NON PUBBLICATO: {len(failed)} file con errori di schema ---")
        for rel, errs in failed:
            print(f"  {rel}")
            for e in errs:
                print(f"    - {e}")
        print(f"\n{CATALOG_PATH.name} resta alla versione precedente. "
              f"Correggi i file elencati e rilancia.")
        raise SystemExit(1)

    catalog = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "num_entries": len(entries),
        "entries": entries,
    }

    # Pubblicazione atomica: si scrive accanto e si sostituisce in un colpo solo.
    # Senza, un'interruzione a metà scrittura lascia un catalogo troncato che il
    # resto della pipeline legge come se fosse valido.
    tmp = CATALOG_PATH.with_suffix(".yaml.tmp")
    try:
        with tmp.open("w", encoding="utf-8") as fp:
            yaml.safe_dump(catalog, fp, sort_keys=False, allow_unicode=True,
                           default_flow_style=False)
        os.replace(tmp, CATALOG_PATH)
    finally:
        tmp.unlink(missing_ok=True)

    print(f"\n--- Riepilogo ---")
    print(f"Research indicizzate: {len(entries)}")
    print(f"Avvisi totali:        {n_warn}")
    print(f"Catalog scritto in:   {CATALOG_PATH}")


if __name__ == "__main__":
    import sys
    if "--scan" in sys.argv:
        scan()
    else:
        main()
