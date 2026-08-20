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

import re
import sqlite3
from datetime import datetime, date
from pathlib import Path

import yaml

from bootstrap_market_data import DB_PATH


KB_DIR = Path.home() / "Claude" / "mercati_finanza" / "knowledge_base"
CATALOG_PATH = KB_DIR / "catalog.yaml"


# Ontologia (Design Document §6.1) — i nove temi ammessi per primary_theme.
ONTOLOGY = {
    "monetary_policy",
    "fiscal_policy",
    "geopolitical",
    "macro_data",
    "corporate_idiosyncratic",
    "regulatory",
    "commodity_energy",
    "financial_stability",
    "structural_themes",
}

REQUIRED_FIELDS = ["title", "date_compiled", "primary_theme",
                   "sub_themes", "relevant_assets", "time_window",
                   "regime_phases", "keywords"]


def get_known_tickers(conn) -> set[str]:
    """Legge dal DB l'elenco dei ticker registrati nella tabella assets."""
    rows = conn.execute("SELECT ticker FROM assets").fetchall()
    return {r[0] for r in rows}


def extract_yaml_block(md_text: str) -> dict | None:
    """
    Estrae il blocco YAML di metadata dalla fine di un file markdown.

    Cerca prima un fenced code block ```yaml ... ``` (preferito per leggibilita');
    se non lo trova, prova un blocco diretto --- ... --- alla fine del file.
    Restituisce un dizionario, o None se non trova nulla di parsabile.
    """
    fenced_blocks = re.findall(
        r"```yaml\s*\n(.*?)\n```", md_text, flags=re.DOTALL
    )
    if fenced_blocks:
        # Prendiamo l'ultimo: la convenzione e' "il blocco metadata sta in fondo".
        raw = fenced_blocks[-1].strip()
        # Rimuovi eventuali --- di apertura/chiusura YAML frontmatter style.
        raw = re.sub(r"^---\s*\n", "", raw)
        raw = re.sub(r"\n---\s*$", "", raw)
        try:
            return yaml.safe_load(raw)
        except yaml.YAMLError as e:
            print(f"  [!] Errore parsing YAML fenced block: {e}")
            return None

    # Fallback: cerca l'ultimo blocco --- ... --- nel file.
    matches = list(re.finditer(r"\n---\s*\n(.*?)\n---\s*(?:\n|$)",
                                md_text, flags=re.DOTALL))
    if matches:
        raw = matches[-1].group(1).strip()
        try:
            return yaml.safe_load(raw)
        except yaml.YAMLError as e:
            print(f"  [!] Errore parsing YAML --- block: {e}")
            return None

    return None


def validate(meta: dict, file_name: str, known_tickers: set[str]) -> list[str]:
    """
    Controlla i metadata di una research. Restituisce una lista di warning
    (stringa vuota se tutto OK).
    """
    warnings = []

    # Campi obbligatori
    for f in REQUIRED_FIELDS:
        if f not in meta:
            warnings.append(f"campo mancante: '{f}'")

    # primary_theme deve essere nell'ontologia
    pt = meta.get("primary_theme")
    if pt and pt not in ONTOLOGY:
        warnings.append(
            f"primary_theme '{pt}' non e' nell'ontologia §6.1 "
            f"(temi ammessi: {sorted(ONTOLOGY)})"
        )

    # Asset rilevanti: warning per ogni ticker non nel DB
    assets = meta.get("relevant_assets", []) or []
    for a in assets:
        if a not in known_tickers:
            warnings.append(
                f"asset '{a}' non e' presente nella tabella 'assets' del DB"
            )

    # date_compiled deve essere una data interpretabile
    dc = meta.get("date_compiled")
    if dc and not isinstance(dc, (date, datetime)):
        warnings.append(
            f"date_compiled '{dc}' non e' una data YAML valida (usa formato YYYY-MM-DD)"
        )

    return warnings


def main():
    if not KB_DIR.exists():
        raise SystemExit(f"Cartella Knowledge Base non trovata: {KB_DIR}")

    # Scansione ricorsiva: ogni studio vive in una propria sottocartella
    # (es. knowledge_base/sovereign_debt/sovereign_debt_crisis.md). I file
    # senza blocco YAML (PDF sorgente esclusi, raw export, ecc.) vengono
    # saltati da extract_yaml_block → nessun falso positivo.
    # Le cartelle/file con prefisso "_" (es. _prompts/) NON sono studi: i prompt
    # template contengono un blocco ```yaml di esempio e altrimenti finirebbero
    # nel catalogo come voci spurie. Convenzione: "_" = non indicizzare.
    md_files = sorted(
        f for f in KB_DIR.rglob("*.md")
        if not any(part.startswith("_") for part in f.relative_to(KB_DIR).parts)
    )
    if not md_files:
        print(f"Nessun file .md trovato in {KB_DIR}")
        return

    conn = sqlite3.connect(DB_PATH)
    try:
        known_tickers = get_known_tickers(conn)
    finally:
        conn.close()

    print(f"=== Costruzione catalog.yaml ===")
    print(f"Scansione di {KB_DIR}")
    print(f"Asset registrati nel DB: {len(known_tickers)}\n")

    entries = []
    total_warnings = 0

    for f in md_files:
        rel = str(f.relative_to(KB_DIR))  # es. "sovereign_debt/sovereign_debt_crisis.md"
        text = f.read_text(encoding="utf-8")
        meta = extract_yaml_block(text)

        if meta is None:
            print(f"  [SKIP]  {rel}: nessun blocco YAML trovato")
            continue

        warns = validate(meta, rel, known_tickers)
        if warns:
            total_warnings += len(warns)
            print(f"  [WARN]  {rel}:")
            for w in warns:
                print(f"            - {w}")
        else:
            print(f"  [OK]    {rel}")

        # Path relativo alla KB come riferimento sorgente (tracciabilita').
        meta_with_source = {"source_file": rel, **meta}
        entries.append(meta_with_source)

    catalog = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "num_entries": len(entries),
        "entries": entries,
    }

    with CATALOG_PATH.open("w", encoding="utf-8") as fp:
        yaml.safe_dump(catalog, fp, sort_keys=False, allow_unicode=True,
                       default_flow_style=False)

    print(f"\n--- Riepilogo ---")
    print(f"Research indicizzate: {len(entries)}")
    print(f"Warning totali:       {total_warnings}")
    print(f"Catalog scritto in:   {CATALOG_PATH}")


if __name__ == "__main__":
    main()
