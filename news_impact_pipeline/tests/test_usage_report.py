#!/usr/bin/env python3
"""usage_report.py — $/scheda utile e $/giornata completata (R14).

Costruisce un usage.csv e un daily_analysis/ finti in una cartella temporanea e
verifica il join: un giorno coi soli tentativi falliti pesa comunque sul totale,
una giornata senza consegna non entra nella media "$/giornata completata".

Non distruttivo: lavora solo dentro una cartella temporanea.
"""
import csv
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import usage_report as ur

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


tmp = Path(tempfile.mkdtemp())
logdir = tmp / "logs"
daily = tmp / "daily_analysis"
logdir.mkdir()
daily.mkdir()
ur.LOGDIR = logdir
ur.DAILY_DIR = daily

FIELDS = ["recorded_at", "started_at", "date", "job", "model", "attempt", "status",
          "turns", "input", "cache_write", "cache_read", "output", "cost_usd",
          "duration_ms"]
with (logdir / "usage.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    # 2026-09-20: un tentativo fallito (nessun costo noto) + uno riuscito, 2 schede,
    # consegnata.
    w.writerow({**dict.fromkeys(FIELDS, ""), "date": "2026-09-20", "job": "daily",
                "status": "interrotto"})
    w.writerow({**dict.fromkeys(FIELDS, ""), "date": "2026-09-20", "job": "daily",
                "status": "ok", "cost_usd": "10.00"})
    # 2026-09-21: un run costoso ma la giornata non è mai stata consegnata (niente
    # _state.json con esito ok) — pesa sul totale, non entra nella media "completata".
    w.writerow({**dict.fromkeys(FIELDS, ""), "date": "2026-09-21", "job": "daily",
                "status": "ok", "cost_usd": "5.00"})

(daily / "2026-09-20").mkdir()
(daily / "2026-09-20" / "news_01.md").write_text("x")
(daily / "2026-09-20" / "news_02.md").write_text("x")
(daily / "2026-09-20" / "_state.json").write_text(json.dumps({"consegna": {"esito": "ok"}}))

(daily / "2026-09-21").mkdir()
(daily / "2026-09-21" / "news_01.md").write_text("x")
# nessun _state.json: giornata non consegnata

righe = ur.build()
check(len(righe) == 2, f"due giornate (ne ha {len(righe)})", str(righe))
r20 = next(r for r in righe if r["date"] == "2026-09-20")
r21 = next(r for r in righe if r["date"] == "2026-09-21")

check(r20["cost"] == 10.0, "il tentativo fallito (costo vuoto) non è sommato come zero né perso",
      str(r20))
check(r20["schede"] == 2 and r20["completata"] is True, "2026-09-20: 2 schede, consegnata", str(r20))
check(r20["per_scheda"] == 5.0, "$/scheda = costo del giorno / schede del giorno", str(r20))

check(r21["completata"] is False, "2026-09-21: nessuna consegna registrata → non completata",
      str(r21))
check(r21["cost"] == 5.0, "il costo di una giornata non consegnata resta nel totale, non sparisce",
      str(r21))

# --since filtra per data
solo_21 = ur.build(since="2026-09-21")
check(len(solo_21) == 1 and solo_21[0]["date"] == "2026-09-21", "--since filtra correttamente",
      str(solo_21))

print(f"\n{'=' * 60}")
print(f"usage_report: {PASS} passati, {FAIL} falliti")
print(f"{'=' * 60}")
sys.exit(1 if FAIL else 0)
