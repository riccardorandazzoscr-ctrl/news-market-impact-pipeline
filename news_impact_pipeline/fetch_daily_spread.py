#!/usr/bin/env python3
"""
fetch_daily_spread.py

Scarica i rendimenti **giornalieri** dei titoli di Stato 10Y di Italia e Germania
da Stooq, calcola lo spread BTP-Bund in basis points e lo salva nel DB sotto il
ticker BTP_BUND_SPREAD — sostituendo la vecchia serie FRED mensile.

Perché: la serie FRED (fetch_fred_data.py) è mensile, inadatta a misurare la
frammentazione eurozona su finestre giornaliere (event study daily, shock periferia).
Stooq fornisce i due rendimenti 10Y daily; lo spread è BTP10Y − Bund10Y, in bps.

Fonte:  Stooq  (simboli 10ity.b = Italia 10Y, 10dey.b = Germania 10Y).
Serve una API key gratuita di Stooq:
    1. Apri  https://stooq.com/q/d/?s=10yity.b  e risolvi il captcha ("Rewrite the above code").
    2. Clicca "Download data in csv file..." — l'URL di download conterrà &apikey=XXXX.
    3. Copia quel valore di apikey e salvalo in ~/Claude/.env:   STOOQ_API_KEY=la_tua_chiave
       (oppure esportalo: export STOOQ_API_KEY=...)

Uso:
    venv/bin/python fetch_daily_spread.py --dry-run   # solo report copertura, NON scrive
    venv/bin/python fetch_daily_spread.py             # scrive (sostituisce) dopo le guardie
    venv/bin/python fetch_daily_spread.py --keep-monthly-before 2014-01-01
        # ibrido: tiene le righe (mensili) prima di quella data, daily da lì in poi
        # (utile se lo storico daily di Stooq non copre i primi anni)
"""

import argparse
import os
import sqlite3
from io import StringIO
from pathlib import Path

import pandas as pd
import urllib.request

from bootstrap_market_data import DB_PATH, create_database

TICKER_SPREAD = "BTP_BUND_SPREAD"
SYM_IT = "10YITY.B"  # Italia 10Y yield (Stooq)
SYM_DE = "10YDEY.B"  # Germania 10Y yield (Stooq)
STOOQ_URL = "https://stooq.com/q/d/l/?s={sym}&i=d&apikey={key}"

# Guardia: non sovrascrivere la serie esistente se il fetch produce meno di tante righe
MIN_ROWS_GUARD = 200


def load_api_key() -> str:
    key = os.environ.get("STOOQ_API_KEY")
    if key:
        return key
    env_file = Path.home() / "Claude" / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("STOOQ_API_KEY="):
                k = line.split("=", 1)[1].strip()
                if k:
                    return k
    raise SystemExit(
        "\nAPI key Stooq non trovata.\n"
        "Ottienila su  https://stooq.com/q/d/?s=10ity.b&get_apikey  e salvala in\n"
        "  ~/Claude/.env   →   STOOQ_API_KEY=la_tua_chiave\n"
    )


def fetch_yield(sym: str, key: str) -> pd.Series:
    """Scarica il CSV daily di un rendimento da Stooq → Series(Close) indicizzata per data.
    Usa uno User-Agent da browser (lo User-Agent di default di urllib viene bloccato
    dal layer anti-bot di Stooq). L'accesso programmatico è sanzionato via apikey."""
    url = STOOQ_URL.format(sym=sym, key=key)
    req = urllib.request.Request(url, headers={
        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/124.0 Safari/537.36"),
        "Accept": "text/csv,text/plain,*/*",
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    if raw.lstrip().lower().startswith("<!doctype") or "<html" in raw[:200].lower():
        raise SystemExit(f"Stooq ha risposto con una pagina di verifica anti-bot per {sym} "
                         "(probabile rate-limit temporaneo): riprovare più tardi.")
    if "apikey" in raw.lower() and "Date" not in raw.split("\n", 1)[0]:
        raise SystemExit(f"Stooq non ha restituito dati per {sym} (key mancante/invalida?).\n{raw[:300]}")
    df = pd.read_csv(StringIO(raw))
    if "Close" not in df.columns or "Date" not in df.columns:
        raise SystemExit(f"Formato CSV inatteso per {sym}: colonne {list(df.columns)}")
    df["Date"] = pd.to_datetime(df["Date"])
    s = df.set_index("Date")["Close"].dropna().sort_index()
    s.name = sym
    return s


def build_spread(key: str) -> pd.DataFrame:
    it = fetch_yield(SYM_IT, key)
    de = fetch_yield(SYM_DE, key)
    print(f"  Italia  10Y: {len(it)} righe, {it.index.min().date()} → {it.index.max().date()}")
    print(f"  Germania10Y: {len(de)} righe, {de.index.min().date()} → {de.index.max().date()}")
    df = pd.concat([it.rename("it"), de.rename("de")], axis=1, sort=True).dropna()
    df["spread"] = (df["it"] - df["de"]) * 100.0   # punti % → bps
    return df


def refresh_daily_spread(dry_run: bool = False, keep_monthly_before: str | None = None) -> int:
    """Scarica e (se non dry-run) sostituisce la serie BTP_BUND_SPREAD daily.
    Restituisce il numero di righe scritte. Sollevabile (SystemExit) su guardia/key.
    Pensata per essere richiamata anche da update_market_data.py."""
    print("=== Fetch spread BTP-Bund DAILY da Stooq ===\n")
    key = load_api_key()
    df = build_spread(key)

    n = len(df)
    print(f"\nSpread daily costruito: {n} righe, "
          f"{df.index.min().date()} → {df.index.max().date()}")
    print("Ultimi 6 valori:")
    for ts, row in df.tail(6).iterrows():
        print(f"  {ts.date()}  spread = {row['spread']:.0f} bps  (IT {row['it']:.2f} − DE {row['de']:.2f})")

    if df.index.min().year > 2011:
        print(f"\n⚠ Lo storico daily parte dal {df.index.min().date()} (> 2011): "
              "una sostituzione secca perderebbe gli anni precedenti. "
              "Valuta --keep-monthly-before per tenere la coda mensile.")

    if dry_run:
        print("\n[dry-run] Nessuna scrittura. Rilancia senza --dry-run per applicare.")
        return 0

    if n < MIN_ROWS_GUARD:
        raise SystemExit(f"\n⛔ Guardia: solo {n} righe (< {MIN_ROWS_GUARD}). "
                         "Non sovrascrivo la serie esistente. Controlla la fonte.")

    conn = sqlite3.connect(DB_PATH)
    try:
        create_database(conn)
        cutoff = keep_monthly_before
        if cutoff:
            conn.execute("DELETE FROM prices WHERE ticker = ? AND date >= ?",
                         (TICKER_SPREAD, cutoff))
            df_to_write = df[df.index >= pd.Timestamp(cutoff)]
            print(f"\nIbrido: tengo le righe < {cutoff}, scrivo daily da {cutoff} in poi "
                  f"({len(df_to_write)} righe).")
        else:
            conn.execute("DELETE FROM prices WHERE ticker = ?", (TICKER_SPREAD,))
            df_to_write = df
            print(f"\nSostituzione completa: cancellate le righe vecchie, scrivo {len(df_to_write)} daily.")

        rows = [
            (TICKER_SPREAD, ts.strftime("%Y-%m-%d"),
             None, None, None,                 # open/high/low — n/a per uno spread
             float(r["spread"]), float(r["spread"]),  # close, adj_close
             None)                             # volume — n/a
            for ts, r in df_to_write.iterrows()
        ]
        conn.executemany("INSERT OR REPLACE INTO prices VALUES (?,?,?,?,?,?,?,?)", rows)
        conn.commit()

        tot = conn.execute("SELECT COUNT(*), MIN(date), MAX(date) FROM prices WHERE ticker=?",
                           (TICKER_SPREAD,)).fetchone()
        print(f"[+] {TICKER_SPREAD}: ora {tot[0]} righe nel DB ({tot[1]} → {tot[2]}).")
        return len(df_to_write)
    finally:
        conn.close()


def backfill_manual(triples, dry_run=False):
    """Inserisce lo spread da rendimenti letti a mano: [(data, IT10Y, DE10Y), ...].

    Serve perché dal 2026-08-19 il download HTTP di Stooq è dietro una sfida
    JavaScript di proof-of-work: il browser la risolve, `urllib` no (404 senza
    User-Agent, pagina di verifica con). Finché non c'è una fonte giornaliera
    alternativa per paese — Eurostat e BCE danno l'Italia solo mensile, la BCE
    dà giornaliero solo la curva AAA aggregata — la via praticabile è aprire
    https://stooq.com/q/d/?s=10yity.b e .../?s=10ydey.b nel browser e passare qui
    le chiusure.

    Prima di scrivere, il metodo viene VALIDATO su una data già presente in DB:
    se lo spread ricalcolato non coincide, non scrive nulla."""
    conn = sqlite3.connect(DB_PATH)
    try:
        create_database(conn)
        rows, control_ok = [], None
        for d, it, de in sorted(triples):
            bps = round((float(it) - float(de)) * 100, 2)
            old = conn.execute("SELECT close FROM prices WHERE ticker=? AND date=?",
                               (TICKER_SPREAD, d)).fetchone()
            if old is not None:
                ok = abs(old[0] - bps) <= 0.51
                control_ok = ok if control_ok is None else (control_ok and ok)
                print(f"  {d}  {bps:7.2f} bps   (già in DB: {old[0]:.2f} → "
                      f"{'coerente' if ok else 'DIVERGE'})")
            else:
                rows.append((TICKER_SPREAD, d, None, None, None, bps, bps, None))
                print(f"  {d}  {bps:7.2f} bps   (nuova)")
        if control_ok is False:
            raise SystemExit("STOP: il ricalcolo non riproduce una riga storica. Nulla scritto.")
        if control_ok is None:
            print("⚠ nessuna data di controllo fra quelle passate: "
                  "includine una già in DB per validare il metodo.")
        if dry_run:
            print(f"\n[dry-run] {len(rows)} righe NON scritte.")
            return
        conn.executemany("INSERT OR REPLACE INTO prices VALUES (?,?,?,?,?,?,?,?)", rows)
        conn.commit()
        t = conn.execute("SELECT COUNT(*), MIN(date), MAX(date) FROM prices WHERE ticker=?",
                         (TICKER_SPREAD,)).fetchone()
        print(f"\nScritte {len(rows)} righe. Serie: {t[0]} righe, {t[1]} → {t[2]}")
    finally:
        conn.close()


def _parse_triple(s):
    d, it, de = s.split(",")
    return d.strip(), float(it), float(de)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="Mostra solo la copertura/anteprima, NON scrive sul DB.")
    ap.add_argument("--keep-monthly-before", metavar="YYYY-MM-DD", default=None,
                    help="Tiene le righe esistenti precedenti a questa data (ibrido).")
    ap.add_argument("--pairs", nargs="+", metavar="YYYY-MM-DD,IT,DE", type=_parse_triple,
                    help="Backfill manuale da rendimenti letti nel browser. "
                         "Includi una data GIÀ in DB come controllo. Es: "
                         "--pairs 2026-08-18,4.077,3.2598 2026-08-19,4.061,3.2620")
    args = ap.parse_args()
    if args.pairs:
        backfill_manual(args.pairs, dry_run=args.dry_run)
        return
    refresh_daily_spread(dry_run=args.dry_run, keep_monthly_before=args.keep_monthly_before)


if __name__ == "__main__":
    main()
