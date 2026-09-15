#!/usr/bin/env python3
"""
update_market_data.py

Aggiornamento INCREMENTALE del database dei prezzi.

Per ogni strumento riscarica una FINESTRA SOVRAPPOSTA che finisce oggi e comincia
qualche giorno prima dell'ultima data gia' in database, poi riscrive quelle righe.
La sovrapposizione serve: una barra scaricata a mercato aperto e' provvisoria, e
ripartendo da "ultima data + 1" non verrebbe mai piu' corretta. E' comunque veloce
(pochi secondi) ed e' pensato per girare ogni giorno via launchd.

Come si esegue a mano (dal Terminale, nella cartella del progetto):
    venv/bin/python update_market_data.py            # aggiornamento normale
    venv/bin/python update_market_data.py --check    # solo diagnosi, nessun download
    venv/bin/python update_market_data.py --deep     # riscarica tutto lo storico
"""

import argparse
from datetime import date, timedelta
import sqlite3
import sys
import time

import pandas as pd
import yfinance as yf

# Riusiamo le definizioni gia' scritte nel bootstrap, per non duplicarle:
# la lista degli asset, il percorso del database e le funzioni di supporto.
from diagnosi_serie import (LOOKBACK_DEFAULT, PONTE_MASSIMO, Problema,  # noqa: F401
                            salto_normale,
                            diagnostica, stampa_diagnosi)
from bootstrap_market_data import (ASSETS, DB_PATH, START_DATE,
                                   create_database, store_prices)


# Quanti giorni di calendario riscaricare PRIMA dell'ultima data gia' in DB.
# Non e' un numero estetico: e' la finestra entro cui quella fonte puo' ancora
# cambiare un valore gia' pubblicato. I future rettificano il settlement il
# giorno dopo; il valutario chiude tardi e la barra di oggi si consolida la
# notte; gli ETF azionari rivedono anche i dividendi.
LOOKBACK_GIORNI = {
    "fx": 5,
    "crypto": 5,
    "equity": 10,
    "fixed_income": 10,
    "volatility": 10,
    "commodity": 10,
}
# La finestra breve non copre le revisioni storiche: quando yfinance ricalcola
# l'adj_close per un dividendo o uno split, cambia TUTTA la serie all'indietro,
# non gli ultimi giorni. Per questo una volta a settimana (sabato, mercati
# chiusi) si riscarica lo storico intero. Stessa cosa a mano con --deep.
GIORNO_DEEP = 5  # 5 = sabato

# Quanto indietro puo' spingersi la riparazione di righe rotte o provvisorie.
# Serve un tetto: una riga che la fonte non sa piu' riempire non deve far
# riscaricare l'intero storico a ogni run.
RIPARAZIONE_MAX_GIORNI = 400

def ultima_data(conn, ticker):
    """Restituisce l'ultima data salvata per un ticker (stringa) o None."""
    row = conn.execute(
        "SELECT MAX(date) FROM prices WHERE ticker = ?", (ticker,)
    ).fetchone()
    return row[0]  # 'AAAA-MM-GG' oppure None se il ticker non c'e' ancora


def finestra_download(conn, asset, oggi, deep=False):
    """Da quale data riscaricare questo ticker, e perche'.

    Tre casi, dal piu' largo al piu' stretto:
    - passata deep (o ticker mai visto): tutto lo storico;
    - ci sono righe da riparare (senza prezzo, o ancora provvisorie): si allarga
      la finestra fino a coprirle, entro RIPARAZIONE_MAX_GIORNI;
    - caso normale: ultima data meno la finestra dello strumento.
    """
    ticker = asset["ticker"]
    last = ultima_data(conn, ticker)
    if deep or last is None:
        return START_DATE, "storico completo"

    lookback = asset.get(
        "lookback_days",
        LOOKBACK_GIORNI.get(asset["asset_class"], LOOKBACK_DEFAULT))
    start = date.fromisoformat(last) - timedelta(days=lookback)
    motivo = f"finestra {lookback}g"

    # Righe da riparare. `status IS NULL` (righe anteriori a questa colonna) NON
    # conta come "da riparare": sono barre vecchie, gia' chiuse. Altrimenti ogni
    # run riscaricherebbe il tetto intero per sempre.
    tetto = (oggi - timedelta(days=RIPARAZIONE_MAX_GIORNI)).isoformat()
    rotta = conn.execute(
        "SELECT MIN(date) FROM prices WHERE ticker = ? AND date >= ? AND "
        "((close IS NULL AND adj_close IS NULL) OR status = 'provisional')",
        (ticker, tetto)).fetchone()[0]
    if rotta and date.fromisoformat(rotta) < start:
        start = date.fromisoformat(rotta)
        motivo = f"riparazione da {rotta}"
    return start.isoformat(), motivo


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="solo diagnosi freschezza/copertura, nessun download")
    ap.add_argument("--deep", action="store_true",
                    help="riscarica tutto lo storico (revisioni di adj_close)")
    args = ap.parse_args()

    if args.check:
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        try:
            problemi = diagnostica(conn, date.today())
        finally:
            conn.close()
        stampa_diagnosi(problemi)
        sys.exit(1 if problemi else 0)

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
        # Passata profonda: a mano con --deep, o da sola il sabato. Riscarica
        # tutto lo storico perche' una revisione di adj_close (dividendo, split)
        # riscrive la serie all'indietro, non solo gli ultimi giorni.
        deep = args.deep or oggi.weekday() == GIORNO_DEEP
        da_aggiornare = [a for a in ASSETS if a["download"]]
        print(f"Aggiornamento incrementale - {oggi.isoformat()}"
              f"{' (passata profonda: storico completo)' if deep else ''}\n")

        righe_totali = 0
        tentativi = 0
        errori = 0
        for a in da_aggiornare:
            ticker = a["ticker"]
            last = ultima_data(conn, ticker)
            start, motivo = finestra_download(conn, a, oggi, deep=deep)

            tentativi += 1
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
                    print(f"  [=] {ticker:<12} la fonte non restituisce nulla da "
                          f"{start} (ultimo in DB: {last})")
                    continue
                # store_prices riscrive le righe della finestra: scarta le barre
                # senza prezzo e marca provvisoria quella di oggi.
                n = store_prices(conn, ticker, df, oggi=oggi.isoformat())
                righe_totali += n
                ultimo_nuovo = df.index.max().strftime("%Y-%m-%d")
                print(f"  [+] {ticker:<12} {n} righe riscritte da {start} "
                      f"al {ultimo_nuovo} ({motivo})")
            except Exception as e:
                errori += 1
                print(f"  [!] {ticker:<12} errore: {e}")
            if deep:
                # 78 richieste di storico intero di fila si prendono un throttle
                # da Yahoo. Stessa pausa del bootstrap, che fa lo stesso giro.
                time.sleep(0.5)

        print(f"\nFatto. Righe scritte (nuove o riscritte): {righe_totali}")
        stampa_diagnosi(diagnostica(conn, oggi))
    finally:
        conn.close()

    # Se OGNI download tentato e' fallito (rete giu', yfinance giu', ecc.) il
    # ciclo sopra non solleva: stampa gli errori e prosegue silenziosamente.
    # Un esito cosi' non e' un aggiornamento riuscito con "nessun dato nuovo",
    # e non deve alimentare spread/crack spread sotto con prezzi non rinfrescati.
    if tentativi > 0 and errori == tentativi:
        print(f"\n[!] Tutti i {tentativi} download falliti: nessun dato aggiornato.")
        sys.exit(1)

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
