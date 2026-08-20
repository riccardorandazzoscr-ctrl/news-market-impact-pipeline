#!/usr/bin/env python3
"""
compute_crack_spread.py — calcola il MARGINE DI RAFFINAZIONE (crack spread 3-2-1).

Perché serve
------------
Quando una raffineria viene colpita (raid ucraini sulle raffinerie russe, attacchi
Houthi, incendi) il canale economico vero NON è il greggio: il greggio può perfino
scendere (meno domanda di input dalla raffineria ferma) mentre benzina e diesel
salgono, perché è la capacità di RAFFINAZIONE a mancare. Con il solo BZ=F quel
canale era invisibile: le schede lo dichiaravano come lacuna da settimane.

Il crack spread è la differenza fra quanto valgono i prodotti e quanto costa il
greggio: è, letteralmente, il margine lordo del raffinatore.

Formula (3-2-1, la convenzione standard)
---------------------------------------
Da 3 barili di greggio la raffineria tipo ricava ~2 di benzina e ~1 di distillato:

    crack ($/bbl) = (2 * RB=F + 1 * HO=F) * 42 / 3  -  BZ=F

RB=F e HO=F quotano in $/GALLONE, il greggio in $/BARILE → il fattore 42
(galloni per barile) converte i prodotti in $/barile. Si divide per 3 perché il
paniere copre 3 barili di greggio.

NB sulla convenzione: usiamo il **Brent** (BZ=F) come greggio invece del WTI. È
una scelta deliberata — il canale che ci interessa è europeo/russo, dove il Brent
è il riferimento. Il 3-2-1 "da manuale" usa il WTI; se un giorno servisse, basta
cambiare CRUDE qui sotto.

Uso: `compute_crack_spread.py [--dry-run]`, oppure importare refresh_crack_spread().
"""

import argparse
import sqlite3

from bootstrap_market_data import DB_PATH

TICKER = "CRACK_321"
GASOLINE = "RB=F"
DISTILLATE = "HO=F"
CRUDE = "BZ=F"
GAL_PER_BBL = 42


def refresh_crack_spread(dry_run: bool = False) -> int:
    """(Ri)calcola l'intera serie CRACK_321 dai prezzi già in DB.

    Ricalcola tutto ogni volta invece di fare un update incrementale: la serie è
    piccola (~3.900 righe) e derivata, quindi un rebuild completo è più semplice e
    non lascia buchi se uno dei tre input viene rivisto a posteriori.
    Restituisce il numero di righe scritte.
    """
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        """
        SELECT g.date,
               COALESCE(g.adj_close, g.close),
               COALESCE(d.adj_close, d.close),
               COALESCE(c.adj_close, c.close)
        FROM prices g
        JOIN prices d ON d.date = g.date AND d.ticker = ?
        JOIN prices c ON c.date = g.date AND c.ticker = ?
        WHERE g.ticker = ?
        ORDER BY g.date
        """,
        (DISTILLATE, CRUDE, GASOLINE),
    ).fetchall()

    out = []
    for dt, gas, dist, crude in rows:
        if gas is None or dist is None or crude is None or crude == 0:
            continue
        crack = (2 * float(gas) + float(dist)) * GAL_PER_BBL / 3 - float(crude)
        out.append((dt, round(crack, 4)))

    print(f"[crack] {len(out)} righe calcolate "
          f"({out[0][0]} → {out[-1][0]})" if out else "[crack] nessun dato")
    if out:
        print("  ultimi 5 valori ($/barile):")
        for dt, v in out[-5:]:
            print(f"    {dt}  {v:8.2f}")

    if dry_run:
        print("[crack] dry-run: nulla scritto.")
        conn.close()
        return len(out)

    conn.execute("DELETE FROM prices WHERE ticker = ?", (TICKER,))
    conn.executemany(
        """INSERT INTO prices(ticker, date, open, high, low, close, adj_close, volume)
           VALUES (?, ?, NULL, NULL, NULL, ?, ?, NULL)""",
        [(TICKER, dt, v, v) for dt, v in out],
    )
    conn.commit()
    conn.close()
    print(f"[crack] scritte {len(out)} righe su {TICKER}.")
    return len(out)


def main():
    p = argparse.ArgumentParser(description="Calcola il crack spread 3-2-1 (margine di raffinazione).")
    p.add_argument("--dry-run", action="store_true", help="calcola e mostra, senza scrivere")
    refresh_crack_spread(dry_run=p.parse_args().dry_run)


if __name__ == "__main__":
    main()
