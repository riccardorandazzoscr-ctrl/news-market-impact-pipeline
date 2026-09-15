"""Finestra sovrapposta, stato della barra e diagnosi delle serie prezzi.

Tutto su un database temporaneo e con DataFrame finti: nessun download, il DB
vero non viene toccato.

    venv/bin/python tests/test_price_updates.py
"""
from datetime import date, timedelta
from pathlib import Path
import sqlite3
import sys
import unittest

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bootstrap_market_data import create_database, store_prices
import update_market_data as umd

OGGI = date(2026, 9, 15)


def barre(righe):
    """righe = [(data, close, adj_close)] -> DataFrame come quello di yfinance."""
    return pd.DataFrame(
        [{"Open": c, "High": c, "Low": c, "Close": c, "Adj Close": a, "Volume": 1}
         for _, c, a in righe],
        index=pd.to_datetime([d for d, _, _ in righe]),
    )


class BarraProvvisoria(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        create_database(self.conn)

    def stato(self, ticker="X"):
        return dict(self.conn.execute(
            "SELECT date, status FROM prices WHERE ticker = ?", (ticker,)))

    def test_la_barra_di_oggi_nasce_provvisoria_quella_di_ieri_e_definitiva(self):
        store_prices(self.conn, "X", barre([("2026-09-14", 10.0, 10.0),
                                            ("2026-09-15", 11.0, 11.0)]),
                     oggi=OGGI.isoformat())
        self.assertEqual(self.stato(),
                         {"2026-09-14": "final", "2026-09-15": "provisional"})

    def test_il_giorno_dopo_la_stessa_barra_diventa_definitiva_col_prezzo_di_chiusura(self):
        store_prices(self.conn, "X", barre([("2026-09-15", 11.0, 11.0)]),
                     oggi=OGGI.isoformat())
        # domani la finestra sovrapposta ripassa sulla stessa data
        store_prices(self.conn, "X", barre([("2026-09-15", 12.5, 12.5)]),
                     oggi=(OGGI + timedelta(days=1)).isoformat())
        riga = self.conn.execute(
            "SELECT close, status, source FROM prices WHERE date = '2026-09-15'"
        ).fetchone()
        self.assertEqual(riga, (12.5, "final", "yfinance"))

    def test_una_barra_senza_prezzo_non_cancella_quella_buona(self):
        store_prices(self.conn, "X", barre([("2026-09-14", 10.0, 10.0)]),
                     oggi=OGGI.isoformat())
        scritte = store_prices(self.conn, "X",
                               barre([("2026-09-14", None, None)]),
                               oggi=OGGI.isoformat())
        self.assertEqual(scritte, 0)
        self.assertEqual(self.conn.execute(
            "SELECT close FROM prices WHERE date = '2026-09-14'").fetchone()[0], 10.0)


class Finestra(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        create_database(self.conn)
        self.asset = {"ticker": "X", "asset_class": "equity"}  # lookback 10g

    def test_la_finestra_torna_indietro_invece_di_ripartire_dal_giorno_dopo(self):
        # il bug di partenza: start = ultima data + 1, e la barra intraday
        # gia' salvata non veniva mai piu' interrogata.
        store_prices(self.conn, "X", barre([("2026-09-15", 11.0, 11.0)]),
                     oggi=OGGI.isoformat())
        start, _ = umd.finestra_download(self.conn, self.asset, OGGI)
        self.assertLessEqual(start, "2026-09-15")
        self.assertEqual(start, "2026-09-05")

    def test_la_finestra_si_allarga_fino_a_una_riga_senza_prezzo(self):
        store_prices(self.conn, "X", barre([("2026-08-01", 9.0, 9.0),
                                            ("2026-09-15", 11.0, 11.0)]),
                     oggi=OGGI.isoformat())
        self.conn.execute("UPDATE prices SET close = NULL, adj_close = NULL "
                          "WHERE date = '2026-08-01'")
        start, motivo = umd.finestra_download(self.conn, self.asset, OGGI)
        self.assertEqual(start, "2026-08-01")
        self.assertIn("riparazione", motivo)

    def test_una_riga_rotta_troppo_vecchia_non_fa_riscaricare_lo_storico(self):
        vecchia = (OGGI - timedelta(days=umd.RIPARAZIONE_MAX_GIORNI + 30)).isoformat()
        store_prices(self.conn, "X", barre([(vecchia, 9.0, 9.0),
                                            ("2026-09-15", 11.0, 11.0)]),
                     oggi=OGGI.isoformat())
        self.conn.execute("UPDATE prices SET close = NULL, adj_close = NULL "
                          "WHERE date = ?", (vecchia,))
        start, _ = umd.finestra_download(self.conn, self.asset, OGGI)
        self.assertEqual(start, "2026-09-05")

    def test_passata_profonda_e_ticker_nuovo_prendono_tutto_lo_storico(self):
        store_prices(self.conn, "X", barre([("2026-09-15", 11.0, 11.0)]),
                     oggi=OGGI.isoformat())
        self.assertEqual(umd.finestra_download(self.conn, self.asset, OGGI,
                                               deep=True)[0], umd.START_DATE)
        self.assertEqual(umd.finestra_download(
            self.conn, {"ticker": "MAI_VISTO", "asset_class": "equity"}, OGGI)[0],
            umd.START_DATE)


class Diagnosi(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        create_database(self.conn)

    def serie(self, ticker, giorni, salta=()):
        """Una seduta per giorno feriale, fino a OGGI meno `giorni` fa."""
        righe = []
        d = OGGI - timedelta(days=giorni)
        while d <= OGGI:
            if d.weekday() < 5 and d.isoformat() not in salta:
                righe.append((d.isoformat(), 10.0, 10.0))
            d += timedelta(days=1)
        store_prices(self.conn, ticker, barre(righe), oggi=OGGI.isoformat())

    def test_serie_sana_nessuna_segnalazione(self):
        self.serie("SANO", 1100)
        self.assertEqual(umd.diagnostica(self.conn, OGGI), [])

    def test_trova_serie_ferma_buco_interno_e_riga_senza_prezzo(self):
        self.serie("FERMO", 1100)
        self.conn.execute("DELETE FROM prices WHERE ticker='FERMO' AND date > ?",
                          ((OGGI - timedelta(days=20)).isoformat(),))
        buco = [(OGGI - timedelta(days=g)).isoformat() for g in range(30, 20, -1)]
        self.serie("BUCO", 1100, salta=set(buco))
        self.serie("ROTTO", 1100)
        self.conn.execute("UPDATE prices SET close=NULL, adj_close=NULL "
                          "WHERE ticker='ROTTO' AND date=?",
                          ((OGGI - timedelta(days=50)).isoformat(),))
        testo = "\n".join(pr.testo for pr in umd.diagnostica(self.conn, OGGI))
        self.assertIn("[freschezza] FERMO", testo)
        self.assertIn("[copertura]  BUCO", testo)
        self.assertIn("[no prezzo]  ROTTO", testo)

    def test_strumento_giovane_soglia_fissa_invece_che_dedotta(self):
        # meno di 250 sedute prima della finestra: la soglia non puo' venire
        # dalla finestra stessa, o il buco alzerebbe la propria soglia.
        corto = [(OGGI - timedelta(days=g)).isoformat() for g in range(60, 45, -1)]
        self.serie("GIOVANE", 200, salta=set(corto))
        self.assertIn("[copertura]  GIOVANE",
                      "\n".join(pr.testo for pr in umd.diagnostica(self.conn, OGGI)))

    def test_trova_la_barra_provvisoria_mai_promossa(self):
        self.serie("APPESO", 1100)
        self.conn.execute("UPDATE prices SET status='provisional' WHERE date=?",
                          ((OGGI - timedelta(days=60)).isoformat(),))
        self.assertIn("[provvisoria] APPESO",
                      "\n".join(pr.testo for pr in umd.diagnostica(self.conn, OGGI)))


class CicloCompleto(unittest.TestCase):
    """Il giro vero (finestra -> download -> scrittura), con yfinance finto."""

    def test_la_barra_provvisoria_di_ieri_viene_riscritta_oggi(self):
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "test.db"
            conn = sqlite3.connect(db)
            create_database(conn)
            # ieri: barra presa a mercato aperto, prezzo provvisorio
            ieri = (date.today() - timedelta(days=1)).isoformat()
            store_prices(conn, "FINTO", barre([(ieri, 100.0, 100.0)]), oggi=ieri)
            conn.close()

            chiuso = barre([(ieri, 123.0, 123.0)])  # la fonte ora da' la chiusura
            asset = [{"ticker": "FINTO", "asset_class": "equity", "download": True,
                      "name": "", "region": "US", "currency": "USD",
                      "source": "yfinance", "description": ""}]
            # Le serie derivate in coda a main() scrivono sul DB VERO: qui si
            # neutralizzano, non sono l'oggetto del test.
            import compute_crack_spread, fetch_daily_spread
            with patch.object(umd, "DB_PATH", db), \
                 patch.object(umd, "ASSETS", asset), \
                 patch.object(umd.yf, "download", return_value=chiuso), \
                 patch.object(compute_crack_spread, "refresh_crack_spread"), \
                 patch.object(fetch_daily_spread, "refresh_daily_spread"), \
                 patch.object(sys, "argv", ["update_market_data.py"]), \
                 patch.object(umd, "date", wraps=date) as finta_data:
                finta_data.today.return_value = date.today()
                umd.main()

            conn = sqlite3.connect(db)
            riga = conn.execute("SELECT close, status FROM prices "
                                "WHERE ticker='FINTO' AND date=?", (ieri,)).fetchone()
            conn.close()
            self.assertEqual(riga, (123.0, "final"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
