#!/usr/bin/env python3
"""
diagnosi_serie.py — dove sta il database dei prezzi, e come si giudica se una serie
e' fresca, bucata o rotta.

Questa diagnosi non scarica niente: legge il DB e basta. Stava dentro
`update_market_data.py`, che per farla importava pandas e yfinance — due secondi e
mezzo di avvio per una domanda che usa solo `sqlite3`. Contava poco finche' a
chiederlo era solo l'aggiornamento dei prezzi, una volta al giorno; da quando
`stato_giornata.py` la interroga a ogni controllo di fase (e ogni 15 secondi mentre
aspetta), il peso dell'import era la parte piu' cara del controllo.

`update_market_data.py` continua a esporre `diagnostica`, `stampa_diagnosi`,
`salto_normale` e `PONTE_MASSIMO` reimportandoli da qui: chi li usava non cambia.
"""

from collections import namedtuple
from datetime import date, timedelta
from pathlib import Path

# --- Dove salviamo il database ----------------------------------------------
# Path.home() e' la cartella utente: cosi' il percorso
# ~/Claude/mercati_finanza/market_data/market_data.db non e' scritto a mano.
# Sta QUI e non in bootstrap_market_data perche' e' l'unica cosa che serve a chi
# vuole solo LEGGERE il database, senza tirarsi dietro il downloader.
# `bootstrap_market_data` lo reimporta, quindi tutti i `from bootstrap_market_data
# import DB_PATH` sparsi nel progetto continuano a funzionare.
DB_DIR = Path.home() / "Claude" / "mercati_finanza" / "market_data"
DB_PATH = DB_DIR / "market_data.db"

# Finestra di riferimento della diagnosi, in anni.
ANNI_DIAGNOSI = 2

# Finestra sovrapposta di default dell'aggiornamento, in giorni. Sta qui e non
# in update_market_data perche' la diagnosi la usa per un giudizio suo: una barra
# ancora 'provisional' piu' vecchia di questa finestra e' stata riscaricata almeno
# una volta senza essere promossa, quindi la fonte non la ripubblica piu'.
# `update_market_data` la reimporta come default dei suoi lookback per classe.
LOOKBACK_DEFAULT = 10

# Ponte di borsa piu' lungo fra i mercati che seguiamo (Capodanno giapponese).
# Serve come soglia di ripiego per uno strumento troppo giovane perche' il suo
# calendario si deduca dalla sua storia.
PONTE_MASSIMO = 9



def salto_normale(giorni, minimo=5):
    """Il ponte festivo piu' lungo che questo strumento fa di suo.

    E' il calendario di borsa dedotto dalla serie stessa, invece di una lista di
    festivita' da mantenere a mano: Capodanno giapponese, Golden Week e Natale
    tedesco durano giorni diversi, e nessuno dei tre e' un buco.

    Si misura sulla storia PRECEDENTE alla finestra esaminata: se la calcolassimo
    sugli stessi giorni che stiamo controllando, un buco alzerebbe la soglia e si
    nasconderebbe da solo.

    ⚠ Cosi' tarata, la soglia trova le interruzioni di piu' giorni, non la singola
    seduta mancante: per quella servirebbe un calendario di borsa vero, che qui
    non c'e'.
    """
    salti = [(b - a).days for a, b in zip(giorni, giorni[1:])]
    return max(minimo, max(salti, default=minimo))


# Una segnalazione di diagnostica, con la sua categoria esplicita.
# La categoria serve a chi deve DECIDERE, non solo a chi stampa: `stato_giornata.py`
# blocca l'analisi sulla sola freschezza delle serie scaricate, mentre copertura,
# righe senza prezzo e barre appese restano avvisi. Prima era tutto una stringa
# formattata, e l'unico modo di distinguerle era rileggerle con una regex --
# esattamente il difetto che questa revisione corregge altrove.
Problema = namedtuple("Problema", "categoria ticker testo")


def diagnostica(conn, oggi, anni=2):
    """Freschezza e copertura per ticker. Sola lettura: non scarica nulla.

    Restituisce la lista dei problemi trovati (vuota = tutto a posto). Il
    conteggio dei ticker non vede niente di tutto questo: un ticker fermo da
    tre settimane e una riga senza prezzo contano come presenti.
    """
    problemi = []
    inizio = (oggi - timedelta(days=365 * anni)).isoformat()
    tickers = [r[0] for r in conn.execute(
        "SELECT DISTINCT ticker FROM prices ORDER BY ticker")]

    for ticker in tickers:
        tutti = [date.fromisoformat(r[0]) for r in conn.execute(
            "SELECT date FROM prices WHERE ticker = ? ORDER BY date", (ticker,))]
        giorni = [d for d in tutti if d.isoformat() >= inizio]
        if len(giorni) < 30:
            problemi.append(Problema("copertura", ticker,
                            f"[copertura]  {ticker:<14} solo {len(giorni)} sedute "
                            f"negli ultimi {anni} anni"))
            continue
        # Soglia dalla storia precedente alla finestra. Se lo strumento e' troppo
        # giovane per averne, si usa la soglia fissa: dedurla dalla finestra che
        # stiamo controllando la renderebbe cieca proprio ai buchi che cerca.
        riferimento = [d for d in tutti if d.isoformat() < inizio]
        normale = (salto_normale(riferimento) if len(riferimento) > 250
                   else PONTE_MASSIMO)
        buchi = [(a, b) for a, b in zip(giorni, giorni[1:]) if (b - a).days > normale]
        if buchi:
            esempi = ", ".join(f"{a}→{b}" for a, b in buchi[:3])
            problemi.append(Problema("copertura", ticker,
                            f"[copertura]  {ticker:<14} {len(buchi)} buchi oltre "
                            f"{normale}g: {esempi}"))
        ritardo = (oggi - giorni[-1]).days
        if ritardo > normale:
            problemi.append(Problema("freschezza", ticker,
                            f"[freschezza] {ticker:<14} fermo al {giorni[-1]} "
                            f"({ritardo}g fa, normale ≤{normale}g)"))

    for ticker, n, prima, ultima in conn.execute(
            "SELECT ticker, COUNT(*), MIN(date), MAX(date) FROM prices "
            "WHERE close IS NULL AND adj_close IS NULL GROUP BY ticker"):
        problemi.append(Problema("no prezzo", ticker,
                        f"[no prezzo]  {ticker:<14} {n} righe senza close ne' "
                        f"adj_close ({prima} → {ultima})"))

    # `status` e' arrivata dopo il primo schema: su un DB non ancora migrato
    # (o su una copia vecchia) la diagnosi deve funzionare lo stesso.
    if "status" not in {r[1] for r in conn.execute("PRAGMA table_info(prices)")}:
        return problemi

    scaduto = (oggi - timedelta(days=LOOKBACK_DEFAULT)).isoformat()
    for ticker, n, ultima in conn.execute(
            "SELECT ticker, COUNT(*), MAX(date) FROM prices "
            "WHERE status = 'provisional' AND date < ? GROUP BY ticker", (scaduto,)):
        problemi.append(Problema("provvisoria", ticker,
                        f"[provvisoria] {ticker:<13} {n} barre mai promosse a "
                        f"definitive (ultima {ultima}): la fonte non le ripubblica"))

    return problemi


def stampa_diagnosi(problemi):
    print("\n--- Freschezza e copertura delle serie ---")
    if not problemi:
        print("  nessun problema: serie fresche, nessun buco, nessuna riga senza prezzo.")
        return
    for p in problemi:
        print(f"  {p.testo}")
    print(f"  ({len(problemi)} segnalazioni. Nessuna e' stata corretta d'ufficio: "
          f"vanno guardate.)")


