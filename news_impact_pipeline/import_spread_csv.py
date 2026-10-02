#!/usr/bin/env python3
"""
import_spread_csv.py

Importa uno spread sovrano contro il Bund da due CSV Stooq scaricati a mano: di default
BTP_BUND_SPREAD (Italia 10Y), con --ticker OAT_BUND_SPREAD la Francia (10YFRY.B).
Serve perché il layer anti-bot JS di Stooq blocca il fetch automatico di fetch_daily_spread.py.

Uso:
    venv/bin/python import_spread_csv.py ~/Downloads/10yity_b_d.csv ~/Downloads/10ydey_b_d.csv
    venv/bin/python import_spread_csv.py IT.csv DE.csv --dry-run
    venv/bin/python import_spread_csv.py FR.csv DE.csv --ticker OAT_BUND_SPREAD
"""

import argparse
import sqlite3
from datetime import date

import pandas as pd

from bootstrap_market_data import DB_PATH, create_database
from fetch_daily_spread import TICKER_SPREAD


def load_csv(path: str) -> pd.Series:
    df = pd.read_csv(path)
    if "Close" not in df.columns or "Date" not in df.columns:
        raise SystemExit(f"Formato CSV inatteso per {path}: colonne {list(df.columns)}")
    df["Date"] = pd.to_datetime(df["Date"])
    return df.set_index("Date")["Close"].dropna().sort_index()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("csv_it", help="CSV Stooq del rendimento Italia 10Y (10YITY.B)")
    ap.add_argument("csv_de", help="CSV Stooq del rendimento Germania 10Y (10YDEY.B)")
    ap.add_argument("--dry-run", action="store_true", help="Mostra l'anteprima, non scrive.")
    ap.add_argument("--ticker", default=TICKER_SPREAD, choices=[TICKER_SPREAD, "OAT_BUND_SPREAD"])
    args = ap.parse_args()

    it = load_csv(args.csv_it)
    de = load_csv(args.csv_de)
    print(f"  Paese   10Y: {len(it)} righe, {it.index.min().date()} → {it.index.max().date()}")
    print(f"  Germania10Y: {len(de)} righe, {de.index.min().date()} → {de.index.max().date()}")

    df = pd.concat([it.rename("it"), de.rename("de")], axis=1, sort=True).dropna()
    df["spread"] = (df["it"] - df["de"]) * 100.0
    # Il CSV di Stooq scaricato a mercati aperti porta la seduta di oggi ancora in corso.
    df = df[df.index < pd.Timestamp(date.today())]

    conn = sqlite3.connect(DB_PATH)
    try:
        create_database(conn)
        existing_max = conn.execute(
            "SELECT MAX(date) FROM prices WHERE ticker=?", (args.ticker,)
        ).fetchone()[0]
        print(f"\nDB attualmente arriva al {existing_max}.")

        new = df[df.index > pd.Timestamp(existing_max)] if existing_max else df
        if new.empty:
            print("Nessuna riga nuova da aggiungere.")
            return
        print(f"Righe nuove da aggiungere: {len(new)}")
        for ts, r in new.iterrows():
            print(f"  {ts.date()}  spread = {r['spread']:.0f} bps  (paese {r['it']:.2f} − DE {r['de']:.2f})")

        if args.dry_run:
            print("\n[dry-run] Nessuna scrittura.")
            return

        conn.executemany(
            "INSERT OR REPLACE INTO prices (ticker, date, open, high, low, close, adj_close, volume, source, status, fetched_at)"
            " VALUES (?,?,?,?,?,?,?,?, 'csv', 'final', datetime('now','localtime'))",
            [
                (args.ticker, ts.strftime("%Y-%m-%d"), None, None, None,
                 float(r["spread"]), float(r["spread"]), None)
                for ts, r in new.iterrows()
            ],
        )
        conn.commit()
        tot = conn.execute(
            "SELECT COUNT(*), MIN(date), MAX(date) FROM prices WHERE ticker=?", (args.ticker,)
        ).fetchone()
        print(f"\n[+] {args.ticker}: ora {tot[0]} righe nel DB ({tot[1]} → {tot[2]}).")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
