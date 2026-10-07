"""Run 11a — definizioni del protocollo «reazione, non seguito» e replay esplorativo (sola lettura)."""
import contextlib
import hashlib
import io
import math
import re
import sqlite3
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import quant_reazione as q

GATE = {"z_min": 2.0, "n_min": 10}
PROTO = {"sigma_window_sessions": 60, "baseline_window_sessions": 250}


def series(n=400, seed=0):
    rng = np.random.default_rng(seed)
    return pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, n))),
                     index=pd.bdate_range("2020-01-01", periods=n), name="AAA")


class Definizioni(unittest.TestCase):
    def test_sigma_vede_solo_le_60_sedute_fino_ad_a_meno_1(self):
        p, a = series().to_numpy().copy(), 300
        s0 = q.sigma(p, a, 60)
        self.assertAlmostEqual(s0, np.std(np.diff(np.log(p[a - 61:a])), ddof=1))
        futuro = p.copy(); futuro[a:] *= 1.5
        self.assertEqual(q.sigma(futuro, a, 60), s0)
        fuori = p.copy(); fuori[a - 62] *= 1.5
        self.assertEqual(q.sigma(fuori, a, 60), s0)
        dentro = p.copy(); dentro[a - 61] *= 1.5
        self.assertNotEqual(q.sigma(dentro, a, 60), s0)
        self.assertIsNone(q.sigma(p, 60, 60))
        self.assertIsNotNone(q.sigma(p, 61, 60))

    def test_reazione_r0_e_z0(self):
        p, a = series().to_numpy().copy(), 300
        p[a - 1], p[a] = 100.0, 102.0
        r0, z0 = q.reaction(p, a, 60)
        self.assertAlmostEqual(r0, 2.0)
        self.assertAlmostEqual(z0, math.log(1.02) / q.sigma(p, a, 60))

    def test_prezzi_non_positivi_escludono_la_cella(self):
        p, a = series().to_numpy().copy(), 300
        zero = p.copy(); zero[a - 5] = 0.0
        self.assertIsNone(q.reaction(zero, a, 60))
        self.assertIsNone(q.baseline(zero, a, 5, 250))
        neg = p.copy(); neg[a] = -1.0
        self.assertIsNone(q.reaction(neg, a, 60))

    def test_baseline_250_finestre_che_finiscono_in_a_meno_1(self):
        p, a = series().to_numpy().copy(), 300
        base = q.baseline(p, a, 5, 250)
        self.assertEqual(len(base), 250)
        self.assertAlmostEqual(base[-1], (p[299] / p[294] - 1) * 100)
        self.assertAlmostEqual(base[0], (p[50] / p[45] - 1) * 100)
        futuro = p.copy(); futuro[a:] *= 1.5
        np.testing.assert_array_equal(q.baseline(futuro, a, 5, 250), base)
        self.assertIsNone(q.baseline(p, 254, 5, 250))
        self.assertIsNotNone(q.baseline(p, 255, 5, 250))

    def test_z_di_tutte_le_sedute_coincide_con_reaction(self):
        s = series()
        p, z = s.to_numpy(), q.abs_z_all_sessions(s, 60)
        self.assertNotIn(s.index[60], z.index)
        for t in (61, 200, 399):
            self.assertAlmostEqual(z.loc[s.index[t]], abs(q.reaction(p, t, 60)[1]))

    def test_indice_di_scostamento(self):
        self.assertAlmostEqual(q.deviation_z(1.0, -0.5, 1.5, 16, 0.2), 0.8 / (2.0 / 1.349 / 4))
        self.assertAlmostEqual(q.deviation_z(1.0, 1.5, -0.5, 16, 0.2), q.deviation_z(1.0, -0.5, 1.5, 16, 0.2))
        self.assertIsNone(q.deviation_z(1.0, 0.3, 0.3, 16, 0.2))

    def test_cancello(self):
        self.assertTrue(q.passes_gate(2.0, 10, GATE))
        self.assertTrue(q.passes_gate(-2.0, 10, GATE))
        self.assertFalse(q.passes_gate(1.99, 10, GATE))
        self.assertFalse(q.passes_gate(2.5, 9, GATE))
        self.assertFalse(q.passes_gate(None, 30, GATE))

    def test_scostamento_indovinato(self):
        self.assertEqual(q.deviation_hit(1.0, 0.2, 0.5), 1)
        self.assertEqual(q.deviation_hit(1.0, 0.2, 0.1), 0)
        self.assertEqual(q.deviation_hit(-1.0, 0.2, -0.3), 1)
        self.assertIsNone(q.deviation_hit(1.0, 0.2, 0.2))
        self.assertIsNone(q.deviation_hit(0.2, 0.2, 1.0))

    def test_voto_per_giorno_e_test_binomiale(self):
        cells = [{"day": "d1", "hit": 1}, {"day": "d1", "hit": 1}, {"day": "d2", "hit": 1},
                 {"day": "d2", "hit": 0}, {"day": "d3", "hit": 0}, {"day": "d4", "hit": 1},
                 {"day": "d4", "hit": None}]
        v = q.daily_votes(cells)
        self.assertEqual(v.to_dict(), {"d1": 1.0, "d2": 0.5, "d3": 0.0, "d4": 1.0})
        self.assertEqual(q.vote_test(v), {"above": 2, "below": 1, "ties": 1, "p": 0.5})

    def test_soglia_critica_del_protocollo(self):
        proto = q.load_protocol()
        k, n, alpha = proto["decision"]["critical_days_above"], proto["decision"]["days"], proto["test"]["alpha"]
        self.assertLessEqual(q.binom_one_sided(k, n), alpha)
        self.assertGreater(q.binom_one_sided(k - 1, n), alpha)
        self.assertEqual((proto["gate"]["z_min"], proto["gate"]["n_min"], proto["primary_horizon_sessions"]),
                         (2.0, 10, 5))


def row(s, pos=300, **kw):
    d = s.index[pos].date().isoformat()
    r = {"scenario": "base", "registration": "", "uso": "", "ingestion_status": "ok",
         "expected_median": "0.8", "hist_p25": "-0.5", "hist_p75": "1.5", "n_analogues": "16",
         "realized_return": "0.5", "anchor_date": d, "made_date": d, "horizon": "5",
         "card_path": f"{d}/news_01.md", "asset": "AAA"}
    r.update(kw)
    return r


class Dati(unittest.TestCase):
    def setUp(self):
        self.s = series()
        self.p = self.s.to_numpy()
        self.prices = lambda asset: self.s if asset == "AAA" else None

    def test_cella_valida_del_ledger(self):
        (c,) = q.ledger_cells([row(self.s)], self.prices, PROTO)
        base = q.baseline(self.p, 300, 5, 250)
        self.assertAlmostEqual(c["normal_median"], float(np.median(base)))
        self.assertAlmostEqual(c["z"], q.deviation_z(0.8, -0.5, 1.5, 16, c["normal_median"]))
        self.assertEqual(c["hit"], q.deviation_hit(0.8, c["normal_median"], 0.5))
        self.assertAlmostEqual(c["realized_prev"], (self.p[304] / self.p[299] - 1) * 100)
        self.assertAlmostEqual(c["z_prev"], q.reaction(self.p, 299, 60)[1])

    def test_righe_escluse_dal_ledger(self):
        sabato = "2021-02-06"   # non è una seduta della serie sintetica
        rows = [row(self.s, registration="recovered"), row(self.s, scenario="escalation"),
                row(self.s, realized_return=""), row(self.s, uso="ritirata"),
                row(self.s, ingestion_status="quarantine"), row(self.s, asset="ZZZ"),
                row(self.s, anchor_date=sabato)]
        self.assertEqual(q.ledger_cells(rows, self.prices, PROTO), [])

    def test_storia_corta_o_banda_mancante_restano_solo_per_la_misura_1(self):
        corta, senza_banda = q.ledger_cells([row(self.s, pos=100), row(self.s, hist_p25="")], self.prices, PROTO)
        self.assertIsNone(corta["normal_median"]); self.assertIsNone(corta["z"]); self.assertIsNone(corta["hit"])
        self.assertIsNone(senza_banda["z"]); self.assertIsNotNone(senza_banda["hit"])

    def test_coppie_della_libreria(self):
        d = self.s.index[300].date().isoformat()
        ep = lambda date, dirs, src="kb:x/y.md": {"date": date, "theme": "t",
                                                  "directions_by_reference": {"AAA": dirs},
                                                  "direction_sources": {"AAA": [src]}}
        eps = [ep(d, ["pos"]), ep(d, ["pos", "neg"]), ep(d, ["neutral"]),
               ep(self.s.index[395].date().isoformat(), ["neg"]), ep("2019-06-01", ["pos"])]
        (c,) = q.library_pairs(eps, self.prices, PROTO)
        self.assertEqual((c["verso"], c["src"]), (1, "kb"))
        self.assertAlmostEqual(c["z0"], q.reaction(self.p, 300, 60)[1])
        self.assertAlmostEqual(c["r5"], (self.p[305] / self.p[300] - 1) * 100)
        (c,) = q.library_pairs([ep(d, ["neg"], "card:2026-10-03/news_03.md")], self.prices, PROTO)
        self.assertEqual((c["verso"], c["src"]), (-1, "card"))

    def test_serie_mensili_assenti_o_con_buchi(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE prices (ticker TEXT, date TEXT, close REAL, adj_close REAL)")
        for i, d in enumerate(pd.bdate_range("2020-01-01", periods=100)):
            conn.execute("INSERT INTO prices VALUES ('DAY', ?, ?, ?)", (d.date().isoformat(), 100 + i, None if i == 7 else 100 + i))
        conn.execute("INSERT INTO prices VALUES ('DAY', '2020-06-01', NULL, NULL)")
        for d in pd.date_range("2015-01-31", periods=60, freq="ME"):
            conn.execute("INSERT INTO prices VALUES ('MON', ?, 1.5, NULL)", (d.date().isoformat(),))
        prices = q.price_loader(conn)
        self.assertEqual(len(prices("DAY")), 100)      # adj mancante → close; riga tutta NULL esclusa
        self.assertIsNone(prices("MON"))
        self.assertIsNone(prices("NONE"))


class Replay(unittest.TestCase):
    @unittest.skipUnless(Path(q.DB_PATH).exists(), "DB prezzi assente")
    def test_replay_sui_dati_del_repo_in_sola_lettura(self):
        prima = hashlib.sha256(q.LEDGER_PATH.read_bytes()).hexdigest()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(q.main(["replay"]), 0)
        out = buf.getvalue()
        self.assertIn("ESPLORATIVO", out)
        for n in range(1, 5):
            self.assertIn(f"## {n}.", out)
        self.assertIsNone(re.search(r"\bnan\b", out))
        self.assertEqual(hashlib.sha256(q.LEDGER_PATH.read_bytes()).hexdigest(), prima)


if __name__ == "__main__":
    unittest.main()
