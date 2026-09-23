#!/usr/bin/env python3
"""record_claude_usage.py — il grezzo di `claude -p --output-format json` diventa
una riga di CSV e due righe di log, con uno schema unico per ogni job (giornaliero,
briefing, mensile: R14).

Perché esiste: il parser è l'unico punto in cui il costo del run viene misurato,
ed è anche l'unico che deve sopravvivere a un grezzo NON-JSON (auth scaduta, crash)
o senza blocco 'usage' — SEMPRE con una riga nel registro, mai il silenzio: un
tentativo fallito che sparisce è indistinguibile da un run gratis, esattamente la
famiglia di guasti muti di references/quando_si_rompe.md.

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


def esegui(contenuto_grezzo, giorno="2026-09-15", job="daily", model="claude-opus-5-5",
           stato=None, csv_path=None, log_path=None, tmp=None):
    """Lancia il parser su un grezzo e restituisce (rc, testo del log, righe del CSV, csv_path)."""
    tmp = tmp or Path(tempfile.mkdtemp())
    raw = tmp / "raw.json"
    log = log_path or (tmp / "run.log")
    csv_path = csv_path or (tmp / "usage.csv")
    raw.write_text(contenuto_grezzo)
    if not log.exists():
        log.write_text("")
    args = [sys.executable, str(SCRIPT), str(raw), str(log), str(csv_path), giorno, job, model]
    if stato:
        args.append(stato)
    rc = subprocess.run(args, capture_output=True, text=True)
    righe = []
    if csv_path.exists():
        with csv_path.open() as f:
            righe = list(csv.DictReader(f))
    return rc, log.read_text(), righe, csv_path


print("\n--- grezzo valido ---")
grezzo = json.dumps({
    "result": "4 schede prodotte.",
    "num_turns": 7,
    "total_cost_usd": 27.9138,
    "duration_ms": 1164000,
    "usage": {"input_tokens": 2573, "cache_creation_input_tokens": 35750,
              "cache_read_input_tokens": 2203776, "output_tokens": 59032},
})
rc, log, righe, _ = esegui(grezzo, job="daily", model="claude-opus-5-5")
check(rc.returncode == 0, "esce 0", rc.stderr)
check("4 schede prodotte." in log, "il testo finale finisce nel log")
check("[usage] turni=7" in log, "la riga di riepilogo riporta i turni", log)
check("costo=$27.91" in log, "il costo è nel log arrotondato a 2 decimali", log)
check(len(righe) == 1, f"il CSV ha 1 riga di dati (ne ha {len(righe)})")
if righe:
    r = righe[0]
    check(r["status"] == "ok", "stato ok", str(r))
    check(r["job"] == "daily" and r["model"] == "claude-opus-5-5", "job e model registrati", str(r))
    check(r["attempt"] == "1", "primo tentativo del giorno", str(r))
    check([r["turns"], r["input"], r["cache_write"], r["cache_read"], r["output"], r["cost_usd"]]
          == ["7", "2573", "35750", "2203776", "59032", "27.9138"],
          "i token e il costo sono quelli giusti", str(r))
    check(r["started_at"] != "", "started_at ricavato da recorded_at - duration_ms", str(r))

print("\n--- grezzo NON JSON (auth scaduta, crash): riga 'errore', non silenzio ---")
rc, log, righe, _ = esegui("Invalid authentication · 401 Not logged in")
check(rc.returncode == 0, "non esplode: esce 0", rc.stderr)
check("Invalid authentication" in log,
      "il grezzo finisce nel log, dove il chiamante lo cerca", log)
check(len(righe) == 1 and righe[0]["status"] == "errore",
      "UNA riga con stato 'errore', non zero righe", str(righe))
check(righe and righe[0]["turns"] == "" and righe[0]["cost_usd"] == "",
      "i campi di consumo restano VUOTI, non diventano 0", str(righe))

print("\n--- grezzo valido ma senza blocco usage: 'incompleto', campi vuoti non zero ---")
rc, log, righe, _ = esegui(json.dumps({"result": "ok", "num_turns": 2}))
check(rc.returncode == 0, "non esplode sui campi mancanti", rc.stderr)
check(len(righe) == 1 and righe[0]["status"] == "incompleto", "stato incompleto", str(righe))
check(righe and righe[0]["turns"] == "2", "i campi noti restano (num_turns)", str(righe))
check(righe and righe[0]["cache_read"] == "" and righe[0]["output"] == "",
      "i campi ignoti sono vuoti, non 0 (0 significherebbe gratis)", str(righe))

print("\n--- run interrotto: stato passato esplicitamente dal chiamante ---")
rc, log, righe, _ = esegui("", stato="interrotto")
check(len(righe) == 1 and righe[0]["status"] == "interrotto",
      "lo stato override vince anche su un grezzo vuoto", str(righe))

print("\n--- tentativi multipli nello stesso giorno: il registro conta da solo ---")
tmp = Path(tempfile.mkdtemp())
csv_path = tmp / "usage.csv"
esegui("", stato="interrotto", giorno="2026-09-20", csv_path=csv_path, tmp=tmp)
_, _, righe, _ = esegui(grezzo, giorno="2026-09-20", csv_path=csv_path, tmp=tmp)
check(len(righe) == 2, f"due righe per lo stesso giorno (ne ha {len(righe)})", str(righe))
if len(righe) == 2:
    check(righe[0]["attempt"] == "1" and righe[1]["attempt"] == "2",
          "il secondo tentativo è numerato 2, nessun contatore esterno da mantenere",
          str(righe))
# Un giorno diverso riparte da 1: l'attempt è per (date, job), non globale.
_, _, righe_altro_giorno, _ = esegui(grezzo, giorno="2026-09-21", csv_path=csv_path, tmp=tmp)
check(righe_altro_giorno[-1]["attempt"] == "1",
      "un giorno diverso riparte da 1 (attempt è per data+job)", str(righe_altro_giorno))

print(f"\n{'=' * 60}")
print(f"record_claude_usage: {PASS} passati, {FAIL} falliti")
print(f"{'=' * 60}")
sys.exit(1 if FAIL else 0)
