#!/usr/bin/env python3
"""Registra un run di `claude -p --output-format json`: testo finale nel log, consumi nel CSV.

Senza questo il costo del run non è misurabile: si potrebbe ricostruire solo
scavando nei transcript di ~/.claude/projects/ (diagnosi del 2026-08-21).
"""

import csv
import json
import sys
from pathlib import Path


def main() -> None:
    raw_path, log_path, csv_path, day = map(Path, sys.argv[1:5])

    try:
        data = json.loads(raw_path.read_text(errors="replace"))
    except Exception:
        # JSON malformato (crash, auth scaduta): riversa il grezzo nel log e basta.
        # Le stringhe d'errore devono restare leggibili: il chiamante ci fa grep
        # sopra per distinguere login scaduto, limite di sessione e 5xx.
        with log_path.open("a") as log:
            log.write(raw_path.read_text(errors="replace"))
        return

    usage = data.get("usage") or {}
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

    new_file = not csv_path.exists()
    with csv_path.open("a", newline="") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(["date", "turns", "input", "cache_write", "cache_read",
                             "output", "cost_usd", "duration_ms"])
        writer.writerow([str(day), turns, tok_in, cache_write, cache_read, tok_out,
                         f"{cost:.4f}", data.get("duration_ms", 0)])


if __name__ == "__main__":
    main()
