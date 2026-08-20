#!/usr/bin/env python3
"""
fetch_fred_data.py

Scarica i rendimenti mensili BTP 10Y (Italia) e Bund 10Y (Germania) dalla
Federal Reserve di St. Louis (FRED) e li salva nel database come spread
BTP-Bund, sotto il ticker BTP_BUND_SPREAD.

I dati FRED sono mensili: ogni riga ha la data dell'ultimo giorno del mese.
Nel layer di analytics questo spread serve come indicatore di regime
(stress periferico eurozona), non per calcolare ritorni giornalieri.

Come si usa:
    1. Ottieni la tua chiave API gratuita su https://fred.stlouisfed.org/docs/api/api_key.html
    2. Salvala in un file di testo: ~/Claude/.env  con il contenuto:
           FRED_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
       oppure esportala nel terminale prima di eseguire:
           export FRED_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    3. Esegui:
           venv/bin/python fetch_fred_data.py
"""

import os
import sqlite3
from datetime import date
from pathlib import Path

import pandas as pd
from fredapi import Fred

from bootstrap_market_data import DB_PATH, create_database


# Serie FRED usate per costruire lo spread
SERIES_BTP  = "IRLTLT01ITM156N"   # Rendimento BTP 10Y Italia (% mensile)
SERIES_BUND = "IRLTLT01DEM156N"   # Rendimento Bund 10Y Germania (% mensile)
TICKER_SPREAD = "BTP_BUND_SPREAD"

START_DATE = "2011-01-01"


def load_api_key() -> str:
    """
    Cerca la chiave FRED_API_KEY in due posti, in ordine:
      1. variabile d'ambiente (export FRED_API_KEY=...)
      2. file ~/Claude/.env  (riga: FRED_API_KEY=...)
    Lancia un errore chiaro se non la trova da nessuna parte.
    """
    key = os.environ.get("FRED_API_KEY")
    if key:
        return key

    env_file = Path.home() / "Claude" / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("FRED_API_KEY="):
                key = line.split("=", 1)[1].strip()
                if key:
                    return key

    raise SystemExit(
        "\nChiave API FRED non trovata.\n"
        "Salvala in ~/Claude/.env con il contenuto:\n"
        "  FRED_API_KEY=la_tua_chiave\n"
        "oppure esportala nel terminale con:\n"
        "  export FRED_API_KEY=la_tua_chiave\n"
        "Poi riesegui lo script."
    )


def fetch_spread(fred: Fred) -> pd.DataFrame:
    """Scarica le due serie e restituisce un DataFrame con la colonna 'spread'.

    I rendimenti FRED sono in % annua. Convertiamo lo spread in basis points
    (1 punto percentuale = 100 bps), che e' la convenzione di mercato
    per il BTP-Bund.
    """
    print(f"  Scarico {SERIES_BTP}  (BTP 10Y Italia)...")
    btp  = fred.get_series(SERIES_BTP,  observation_start=START_DATE)
    print(f"  Scarico {SERIES_BUND} (Bund 10Y Germania)...")
    bund = fred.get_series(SERIES_BUND, observation_start=START_DATE)

    spread = ((btp - bund) * 100).dropna()  # da punti percentuali a basis points
    spread.name = "spread"
    return spread.to_frame()


def ultima_data_fred(conn) -> str | None:
    """Ultima data gia' salvata per BTP_BUND_SPREAD nel database."""
    row = conn.execute(
        "SELECT MAX(date) FROM prices WHERE ticker = ?", (TICKER_SPREAD,)
    ).fetchone()
    return row[0]


def store_spread(conn, df: pd.DataFrame, from_date: str | None = None) -> int:
    """
    Salva le righe dello spread nel database.
    Se from_date e' fornita, scarta tutto cio' che e' uguale o precedente.
    Restituisce il numero di righe inserite.
    """
    rows = []
    for timestamp, row in df.iterrows():
        date_str = timestamp.strftime("%Y-%m-%d")
        if from_date and date_str <= from_date:
            continue
        value = None if pd.isna(row["spread"]) else float(row["spread"])
        rows.append((
            TICKER_SPREAD,
            date_str,
            None,   # open  — non applicabile
            None,   # high  — non applicabile
            None,   # low   — non applicabile
            value,  # close — usiamo 'close' per lo spread
            value,  # adj_close — uguale a close per i rendimenti
            None,   # volume — non applicabile
        ))

    if rows:
        conn.executemany(
            "INSERT OR REPLACE INTO prices VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows
        )
        conn.commit()
    return len(rows)


def main():
    print("=== Fetch spread BTP-Bund da FRED ===\n")

    api_key = load_api_key()
    fred = Fred(api_key=api_key)

    conn = sqlite3.connect(DB_PATH)
    try:
        create_database(conn)

        last = ultima_data_fred(conn)
        if last:
            print(f"Ultimo valore gia' presente: {last}. Scarico solo i dati successivi.\n")
        else:
            print(f"Nessun dato presente. Scarico tutto dal {START_DATE}.\n")

        df = fetch_spread(fred)

        n = store_spread(conn, df, from_date=last)

        if n == 0:
            print(f"\nNessuna riga nuova da aggiungere (dati gia' aggiornati).")
        else:
            primo  = df.index.min().strftime("%Y-%m-%d")
            ultimo = df.index.max().strftime("%Y-%m-%d")
            print(f"\n[+] {TICKER_SPREAD}: +{n} righe "
                  f"({'storico dal ' + primo if not last else 'nuovi valori'} fino al {ultimo})")

        # Mostra gli ultimi 6 mesi come controllo visivo
        print("\nUltimi 6 valori nel database:")
        rows = conn.execute(
            "SELECT date, close FROM prices WHERE ticker = ? "
            "ORDER BY date DESC LIMIT 6", (TICKER_SPREAD,)
        ).fetchall()
        for r in rows:
            print(f"  {r[0]}  spread = {r[1]:.0f} bps" if r[1] is not None else f"  {r[0]}  spread = N/A")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
