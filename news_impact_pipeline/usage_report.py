#!/usr/bin/env python3
"""usage_report.py — costo per SCHEDA UTILE e per GIORNATA COMPLETATA (R14).

Non un altro numero scritto a mano nei documenti (CLAUDE.md lo vieta: un dato che
cambia si interroga, non si trascrive): unisce `logs/usage.csv` (tutti i tentativi
del giorno — coordinamento e retry compresi, non solo il run che è andato a buon
fine) con `daily_analysis/<data>/` (quante schede, se la giornata è stata
consegnata). Un run con costo ma zero schede pesa comunque sul totale: non sparisce.

Uso:
    venv/bin/python usage_report.py                 # tutte le date in usage.csv
    venv/bin/python usage_report.py --since 2026-09-01
"""

import argparse
import csv
import json
from pathlib import Path

LOGDIR = Path(__file__).resolve().parent / "logs"
DAILY_DIR = Path(__file__).resolve().parent.parent / "daily_analysis"


def read_usage(csv_path: Path) -> dict[str, float]:
    """date -> costo totale (somma di TUTTI i tentativi con un costo noto)."""
    tot: dict[str, float] = {}
    if not csv_path.exists():
        return tot
    with csv_path.open(newline="") as f:
        for row in csv.DictReader(f):
            cost = row.get("cost_usd") or ""
            if cost == "":
                continue
            tot[row["date"]] = tot.get(row["date"], 0.0) + float(cost)
    return tot


def n_schede(date: str) -> int:
    d = DAILY_DIR / date
    return len(list(d.glob("news_*.md"))) if d.is_dir() else 0


def consegnata(date: str) -> bool:
    state = DAILY_DIR / date / "_state.json"
    if not state.exists():
        return False
    try:
        data = json.loads(state.read_text())
    except Exception:
        return False
    return (data.get("consegna") or {}).get("esito") == "ok"


def build(since: str | None = None) -> list[dict]:
    tot = read_usage(LOGDIR / "usage.csv")
    rows = []
    for date, cost in sorted(tot.items()):
        if since and date < since:
            continue
        schede = n_schede(date)
        rows.append({
            "date": date, "cost": cost, "schede": schede,
            "per_scheda": (cost / schede) if schede else None,
            "completata": consegnata(date),
        })
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--since", default=None, metavar="YYYY-MM-DD")
    args = ap.parse_args()

    rows = build(args.since)
    if not rows:
        print("Nessun dato in usage.csv.")
        return

    print(f"{'data':<12} {'costo':>8} {'schede':>7} {'$/scheda':>10}  completata")
    for r in rows:
        per = f"{r['per_scheda']:.2f}" if r["per_scheda"] is not None else "n/a"
        print(f"{r['date']:<12} {r['cost']:>8.2f} {r['schede']:>7} {per:>10}  "
              f"{'sì' if r['completata'] else 'no'}")

    completate = [r for r in rows if r["completata"]]
    con_schede = [r for r in rows if r["schede"]]
    print()
    print(f"Totale: ${sum(r['cost'] for r in rows):.2f} su {len(rows)} giornate.")
    if con_schede:
        media_scheda = sum(r["cost"] for r in con_schede) / sum(r["schede"] for r in con_schede)
        print(f"$/scheda utile (media pesata): ${media_scheda:.2f}")
    if completate:
        media_giornata = sum(r["cost"] for r in completate) / len(completate)
        print(f"$/giornata completata (media): ${media_giornata:.2f} "
              f"({len(completate)}/{len(rows)} giornate consegnate)")


if __name__ == "__main__":
    main()
