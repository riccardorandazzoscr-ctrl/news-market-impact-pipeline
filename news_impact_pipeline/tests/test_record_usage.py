#!/usr/bin/env python3
"""record_claude_usage.py — il grezzo di `claude -p --output-format json` diventa
una riga di CSV e due righe di log.

Perché esiste: il parser è l'unico punto in cui il costo del run viene misurato,
ed è anche l'unico che deve sopravvivere a un grezzo NON-JSON (auth scaduta, crash).
Se ingoia un errore in silenzio, il run risulta gratis e il guasto invisibile —
esattamente la famiglia di guasti muti di references/quando_si_rompe.md.

Non distruttivo: lavora solo dentro una cartella temporanea.
"""

import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "record_claude_usage.py"
PASS = FAIL = 0


def check(cond, descr, extra=""):
    global PASS, FAIL
    if cond:
        print(f"  ✓ {descr}")
        PASS += 1
    else:
        print(f"  ✗ {descr}")
        if extra:
            print(f"      {extra}")
        FAIL += 1


def esegui(contenuto_grezzo, giorno="2026-09-15"):
    """Lancia il parser su un grezzo e restituisce (testo del log, righe del CSV)."""
    tmp = Path(tempfile.mkdtemp())
    raw, log, csv_path = tmp / "raw.json", tmp / "run.log", tmp / "usage.csv"
    raw.write_text(contenuto_grezzo)
    log.write_text("")
    rc = subprocess.run([sys.executable, str(SCRIPT), str(raw), str(log),
                         str(csv_path), giorno], capture_output=True, text=True)
    righe = []
    if csv_path.exists():
        with csv_path.open() as f:
            righe = list(csv.reader(f))
    return rc, log.read_text(), righe


print("\n--- grezzo valido ---")
grezzo = json.dumps({
    "result": "4 schede prodotte.",
    "num_turns": 7,
    "total_cost_usd": 27.9138,
    "duration_ms": 1164000,
    "usage": {"input_tokens": 2573, "cache_creation_input_tokens": 35750,
              "cache_read_input_tokens": 2203776, "output_tokens": 59032},
})
rc, log, righe = esegui(grezzo)
check(rc.returncode == 0, "esce 0", rc.stderr)
check("4 schede prodotte." in log, "il testo finale finisce nel log")
check("[usage] turni=7" in log, "la riga di riepilogo riporta i turni", log)
check("costo=$27.91" in log, "il costo è nel log arrotondato a 2 decimali", log)
check(len(righe) == 2, f"il CSV ha intestazione + 1 riga (ne ha {len(righe)})")
if len(righe) == 2:
    intestazione, riga = righe
    atteso = ["2026-09-15", "7", "2573", "35750", "2203776", "59032",
              "27.9138", "1164000"]
    check(riga == atteso, "la riga del CSV ha i valori giusti nell'ordine giusto",
          f"atteso {atteso}\n      ottenuto {riga}")
    check(intestazione[0] == "date" and intestazione[6] == "cost_usd",
          "l'intestazione è quella storica di usage.csv", str(intestazione))

print("\n--- grezzo NON JSON (auth scaduta, crash) ---")
# Il caso che conta: deve riversare il grezzo nel log perché il chiamante ci
# faccia grep sopra ("Invalid authentication", "session limit", "529"), NON
# sparire in silenzio e NON scrivere una riga di costo finta.
rc, log, righe = esegui("Invalid authentication · 401 Not logged in")
check(rc.returncode == 0, "non esplode: esce 0", rc.stderr)
check("Invalid authentication" in log,
      "il grezzo finisce nel log, dove il chiamante lo cerca", log)
check(righe == [], "nessuna riga di consumo inventata", str(righe))

print("\n--- grezzo valido ma senza blocco usage ---")
rc, log, righe = esegui(json.dumps({"result": "ok"}))
check(rc.returncode == 0, "non esplode sui campi mancanti", rc.stderr)
check(len(righe) == 2 and righe[1][1:6] == ["0", "0", "0", "0", "0"],
      "i campi assenti valgono 0, non saltano la colonna", str(righe))

print(f"\n{'=' * 60}")
print(f"record_claude_usage: {PASS} passati, {FAIL} falliti")
print(f"{'=' * 60}")
sys.exit(1 if FAIL else 0)
