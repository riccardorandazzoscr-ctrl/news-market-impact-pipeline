#!/usr/bin/env python3
"""
update_market_data.py

Aggiornamento INCREMENTALE del database dei prezzi.

Per ogni strumento guarda l'ultima data gia' presente nel database e scarica
da yfinance solo i giorni successivi, poi li aggiunge. E' veloce (pochi secondi)
ed e' pensato per essere eseguito ogni giorno, anche in automatico via launchd.

Come si esegue a mano (dal Terminale, nella cartella del progetto):
    venv/bin/python update_market_data.py
"""

from datetime import date, timedelta
import sqlite3

import pandas as pd
import yfinance as yf

# Riusiamo le definizioni gia' scritte nel bootstrap, per non duplicarle:
# la lista degli asset, il percorso del database e le funzioni di supporto.
from bootstrap_market_data import ASSETS, DB_PATH, create_database, store_prices


def ultima_data(conn, ticker):
    """Restituisce l'ultima data salvata per un ticker (stringa) o None."""
    row = conn.execute(
        "SELECT MAX(date) FROM prices WHERE ticker = ?", (ticker,)
    ).fetchone()
    return row[0]  # 'AAAA-MM-GG' oppure None se il ticker non c'e' ancora


def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        create_database(conn)  # innocuo se le tabelle esistono gia'

        # Sincronizza il REGISTRO `assets` con la lista nel codice: se si aggiunge
        # un asset in bootstrap (ASSETS) e si lancia solo questo update, il registro
        # resterebbe stale (i prezzi entrano ma l'anagrafica no) → build_catalog e i
        # validatori lo vedrebbero "non in DB". Upsert idempotente, niente prezzi.
        conn.executemany(
            "INSERT OR REPLACE INTO assets "
            "(ticker,name,asset_class,region,currency,source,description) "
            "VALUES (?,?,?,?,?,?,?)",
            [(a["ticker"], a["name"], a["asset_class"], a["region"],
              a["currency"], a["source"], a["description"]) for a in ASSETS]
        )
        conn.commit()

        oggi = date.today()
        da_aggiornare = [a for a in ASSETS if a["download"]]
        print(f"Aggiornamento incrementale - {oggi.isoformat()}\n")

        nuove_totali = 0
        for a in da_aggiornare:
            ticker = a["ticker"]
            last = ultima_data(conn, ticker)

            # Da quale giorno ripartire: il giorno DOPO l'ultimo salvato.
            if last is None:
                start = "2011-01-01"  # ticker mai scaricato: prendi tutto
            else:
                start = (date.fromisoformat(last) + timedelta(days=1)).isoformat()

            # Se l'ultimo dato e' gia' di oggi (o futuro), non c'e' nulla da fare.
            if start > oggi.isoformat():
                print(f"  [-] {ticker:<12} gia' aggiornato (ultimo: {last})")
                continue

            try:
                df = yf.download(
                    ticker,
                    start=start,
                    end=(oggi + timedelta(days=1)).isoformat(),  # +1 = include oggi
                    auto_adjust=False,
                    progress=False,
                    threads=False,
                )
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                if df.empty:
                    print(f"  [=] {ticker:<12} nessun dato nuovo (ultimo: {last})")
                    continue
                n = store_prices(conn, ticker, df)
                nuove_totali += n
                ultimo_nuovo = df.index.max().strftime("%Y-%m-%d")
                print(f"  [+] {ticker:<12} +{n} righe (fino al {ultimo_nuovo})")
            except Exception as e:
                print(f"  [!] {ticker:<12} errore: {e}")

        print(f"\nFatto. Nuove righe aggiunte: {nuove_totali}")
    finally:
        conn.close()

    # Spread BTP-Bund (Stooq): rinfresco SETTIMANALE, solo il lunedi'.
    # Motivo: Stooq blocca con verifica anti-bot se riceve troppe richieste ravvicinate;
    # 1 richiesta/settimana resta sotto la soglia. Lo spread e' un indicatore di regime
    # a lenta variazione, quindi la cadenza settimanale e' sufficiente. Resiliente:
    # un errore qui (rete/key/anti-bot Stooq) NON deve compromettere l'update sopra.
    if date.today().weekday() == 0:  # 0 = lunedi'
        try:
            from fetch_daily_spread import refresh_daily_spread
            print("\n--- Refresh spread BTP-Bund (Stooq, settimanale/lunedi') ---")
            refresh_daily_spread()
        except SystemExit as e:
            print(f"  [!] BTP_BUND_SPREAD non aggiornato (guardia/key/anti-bot): {e}")
        except Exception as e:
            print(f"  [!] BTP_BUND_SPREAD non aggiornato (errore Stooq): {e}")
    else:
        print("\n[-] Spread BTP-Bund: rinfresco solo il lunedi' (oggi salto).")

    # Crack spread 3-2-1 (margine di raffinazione): OGNI GIORNO, a differenza del
    # BTP-Bund. Nessuna fonte esterna da interrogare — si ricalcola dai prezzi
    # RB=F/HO=F/BZ=F appena aggiornati sopra, quindi niente anti-bot ne' rate limit.
    # Resiliente: un errore qui non deve compromettere l'update dei prezzi.
    try:
        from compute_crack_spread import refresh_crack_spread
        print("\n--- Ricalcolo crack spread 3-2-1 (margine di raffinazione) ---")
        refresh_crack_spread()
    except Exception as e:
        print(f"  [!] CRACK_321 non aggiornato: {e}")


if __name__ == "__main__":
    main()
