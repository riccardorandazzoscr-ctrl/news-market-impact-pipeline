#!/usr/bin/env python3
"""Record a Codex JSONL run without confusing token usage with API cost."""

import csv
import json
import sys
from pathlib import Path


def main() -> None:
    raw_path, log_path, csv_path, day = map(Path, sys.argv[1:5])
    messages = []
    errors = []
    totals = {"input_tokens": 0, "cached_input_tokens": 0,
              "output_tokens": 0, "reasoning_output_tokens": 0}
    turns = 0
    for line in raw_path.read_text(errors="replace").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            errors.append(line)
            continue
        kind = event.get("type")
        item = event.get("item") or {}
        if kind == "item.completed" and item.get("type") == "agent_message":
            messages.append(item.get("text", ""))
        elif kind == "item.completed" and item.get("type") == "error":
            errors.append(item.get("message", "Errore Codex senza dettagli"))
        elif kind == "turn.completed":
            turns += 1
            usage = event.get("usage") or {}
            for key in totals:
                totals[key] += usage.get(key, 0) or 0
        elif kind in {"turn.failed", "error"}:
            errors.append(json.dumps(event, ensure_ascii=False))

    with log_path.open("a") as log:
        if messages:
            log.write(messages[-1] + "\n")
        for error in errors:
            log.write(error + "\n")
        log.write(f"[codex usage] turni={turns} input={totals['input_tokens']} "
                  f"cache_read={totals['cached_input_tokens']} "
                  f"output={totals['output_tokens']} "
                  "costo API=n.d. (accesso ChatGPT)\n")

    new_file = not csv_path.exists()
    with csv_path.open("a", newline="") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(["date", "turns", *totals.keys()])
        writer.writerow([str(day), turns, *totals.values()])


if __name__ == "__main__":
    main()
