#!/usr/bin/env python3
"""Registra un'esecuzione di `claude -p --output-format json` in un CSV di consumi.

Uno schema unico per tutti i job (`record_claude_usage.py ... <job> <model>`), non
uno diverso per giornaliero e briefing: prima il mensile non lasciava traccia (R14).

Un grezzo non-JSON o senza blocco 'usage' produce comunque una riga — stato
'errore'/'incompleto', mai il silenzio: senza questo il costo del run non è
misurabile se non scavando nei transcript (diagnosi del 2026-08-21), e "nessun
dato di usage" non deve poter significare "nessun consumo"
(references/quando_si_rompe.md). I campi che non si conoscono restano VUOTI, non
diventano 0: uno zero è indistinguibile da un run davvero gratis.
"""

import csv
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

FIELDS = ["recorded_at", "started_at", "date", "job", "model", "attempt", "status",
          "turns", "input", "cache_write", "cache_read", "output", "cost_usd",
          "duration_ms"]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _next_attempt(csv_path: Path, date: str, job: str) -> int:
    """Quante righe precedenti esistono già per (date, job): non serve un contatore
    esterno, il registro stesso sa a che tentativo siamo."""
    if not csv_path.exists():
        return 1
    with csv_path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    return 1 + sum(1 for r in rows if r.get("date") == date and r.get("job") == job)


def _write_row(csv_path: Path, row: dict) -> None:
    new_file = not csv_path.exists()
    with csv_path.open("a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 6:
        sys.exit("uso: record_claude_usage.py <raw.json> <log> <csv> <date> <job> <model> [stato]")
    raw_path, log_path, csv_path = Path(args[0]), Path(args[1]), Path(args[2])
    day, job, model = args[3], args[4], args[5]
    stato_override = args[6] if len(args) > 6 else ""

    base = {"recorded_at": _now_iso(), "date": day, "job": job, "model": model,
            "attempt": _next_attempt(csv_path, day, job)}
    vuota = {"started_at": "", "turns": "", "input": "", "cache_write": "",
             "cache_read": "", "output": "", "cost_usd": "", "duration_ms": ""}

    try:
        data = json.loads(raw_path.read_text(errors="replace"))
    except Exception:
        # JSON malformato (crash, auth scaduta, run ucciso a metà): il grezzo resta
        # leggibile nel log — il chiamante ci fa grep sopra per distinguere login
        # scaduto, limite di sessione e 5xx — ma qui scriviamo COMUNQUE una riga:
        # un tentativo fallito non deve sparire dal registro.
        with log_path.open("a") as log:
            log.write(raw_path.read_text(errors="replace"))
        _write_row(csv_path, {**base, **vuota, "status": stato_override or "errore"})
        return

    usage = data.get("usage") or {}
    duration_ms = data.get("duration_ms")
    started_at = ""
    if duration_ms:
        started_at = (datetime.fromisoformat(base["recorded_at"])
                       - timedelta(milliseconds=duration_ms)).isoformat(timespec="seconds")

    if not usage:
        # JSON valido ma senza il blocco che conta i token: non è un run gratis,
        # è un run di cui non sappiamo il consumo. I campi restano vuoti.
        with log_path.open("a") as log:
            log.write((data.get("result") or "") + "\n")
            log.write("[usage] nessun blocco 'usage' nel grezzo: consumo sconosciuto.\n")
        _write_row(csv_path, {**base, **vuota, "status": stato_override or "incompleto",
                               "started_at": started_at,
                               "turns": data.get("num_turns", ""),
                               "cost_usd": data.get("total_cost_usd", ""),
                               "duration_ms": duration_ms or ""})
        return

    cache_read = usage.get("cache_read_input_tokens", 0) or 0
    cache_write = usage.get("cache_creation_input_tokens", 0) or 0
    tok_in = usage.get("input_tokens", 0) or 0
    tok_out = usage.get("output_tokens", 0) or 0
    turns = data.get("num_turns", 0) or 0
    cost = data.get("total_cost_usd", 0.0) or 0.0

    with log_path.open("a") as log:
        log.write((data.get("result") or "") + "\n")
        log.write(f"[usage] turni={turns} input={tok_in} cache_write={cache_write} "
                  f"cache_read={cache_read} output={tok_out} costo=${cost:.2f}\n")

    _write_row(csv_path, {**base, "status": stato_override or "ok",
                           "started_at": started_at, "turns": turns, "input": tok_in,
                           "cache_write": cache_write, "cache_read": cache_read,
                           "output": tok_out, "cost_usd": f"{cost:.4f}",
                           "duration_ms": duration_ms or 0})


if __name__ == "__main__":
    main()
