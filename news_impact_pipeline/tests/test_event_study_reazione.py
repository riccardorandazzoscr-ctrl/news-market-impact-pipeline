"""Run 11b — reazione degli analoghi, reazione di oggi e seguito accanto al normale in event_study.py."""
import sqlite3
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import event_study as es
import quant_reazione as q

W = [1, 3, 5, 10]


def series(n=500, seed=0):
    rng = np.random.default_rng(seed)
    return pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, n))),
                     index=pd.bdate_range("2020-01-01", periods=n), name="AAA")


def con_mosse(mosse: dict[int, float], n=500) -> pd.Series:
    """Serie sintetica in cui la seduta `pos` fa esattamente `pct`% sulla precedente."""
    s = series(n)
    p = s.to_numpy().copy()
    for pos, pct in sorted(mosse.items()):
        p[pos:] *= (p[pos - 1] * (1 + pct / 100)) / p[pos]
    return pd.Series(p, index=s.index, name="AAA")


def giorno(s: pd.Series, pos: int) -> date:
    return s.index[pos].date()


class Definizioni(unittest.TestCase):
    def test_una_sola_definizione_condivisa_col_replay(self):
        self.assertIs(q.sigma, es.sigma)
        self.assertIs(q.reaction, es.reaction)
        self.assertIs(q.baseline, es.baseline)


class ReazioneAnaloghi(unittest.TestCase):
    def setUp(self):
        self.s = con_mosse({300: 2.0, 350: -1.0, 400: 4.0})
        self.ancore = [giorno(self.s, i) for i in (300, 350, 400)]

    def test_r0_mediana_e_quartili_delle_sedute_ancora(self):
        b = es.reaction_blocks(self.s, self.ancore, W)
        self.assertEqual(b["n"], 3)
        self.assertAlmostEqual(b["r0_median"], 2.0)
        self.assertAlmostEqual(b["r0_p25"], 0.5)
        self.assertAlmostEqual(b["r0_p75"], 3.0)

    def test_z_mediano_usa_la_sigma_delle_60_sedute_prima_dell_ancora(self):
        b = es.reaction_blocks(self.s, self.ancore, W)
        p = self.s.to_numpy()
        attesi = [abs(es.reaction(p, a, 60)[1]) for a in (300, 350, 400)]
        self.assertAlmostEqual(b["abs_z_median"], float(np.median(attesi)))

    def test_verso_coerente_solo_se_il_verso_e_dichiarato(self):
        self.assertIsNone(es.reaction_blocks(self.s, self.ancore, W)["coherent"])
        self.assertEqual(es.reaction_blocks(self.s, self.ancore, W, direction="pos")["coherent"], (2, 3))
        self.assertEqual(es.reaction_blocks(self.s, self.ancore, W, direction="neg")["coherent"], (1, 3))

    def test_ancora_senza_60_sedute_di_storia_resta_fuori(self):
        b = es.reaction_blocks(self.s, [giorno(self.s, 30)] + self.ancore, W)
        self.assertEqual(b["n"], 3)


class ReazioneDiOggi(unittest.TestCase):
    def setUp(self):
        self.ancore_pos = (300, 350, 400)

    def blocco(self, mossa_oggi, seduta_pos=480):
        s = con_mosse({300: 2.0, 350: -1.0, 400: 4.0, 480: mossa_oggi})
        ancore = [giorno(s, i) for i in self.ancore_pos]
        return s, es.reaction_blocks(s, ancore, W, session=giorno(s, seduta_pos))

    def test_mossa_piu_grande_di_tutti_gli_analoghi(self):
        s, b = self.blocco(9.0)
        t = b["today"]
        self.assertAlmostEqual(t["r0"], 9.0)
        self.assertAlmostEqual(t["z0"], es.reaction(s.to_numpy(), 480, 60)[1])
        self.assertEqual(t["pct_abs"], 100)
        self.assertEqual(t["pct_signed"], 100)
        self.assertEqual(t["label"], "più forte degli analoghi")

    def test_mossa_piu_piccola_di_tutti_gli_analoghi(self):
        _, b = self.blocco(0.01)
        self.assertEqual(b["today"]["pct_abs"], 0)
        self.assertEqual(b["today"]["label"], "più debole degli analoghi")

    def test_mossa_in_mezzo_agli_analoghi(self):
        _, b = self.blocco(-2.0)          # |z| fra quelli di −1% e di +4%... a parità di σ: 2 su 3 sotto
        self.assertEqual(b["today"]["label"], "in linea con gli analoghi")
        self.assertEqual(b["today"]["pct_signed"], 0)   # più negativa di ogni analogo

    def test_seduta_senza_prezzo_non_inventa_una_reazione(self):
        s = con_mosse({300: 2.0})
        b = es.reaction_blocks(s, [giorno(s, 300)], W, session=date(2030, 1, 1))
        self.assertEqual(b["today"], {"session": date(2030, 1, 1), "missing": True})

    def test_senza_seduta_il_blocco_non_c_e(self):
        s = con_mosse({300: 2.0})
        self.assertIsNone(es.reaction_blocks(s, [giorno(s, 300)], W)["today"])


class SeguitoControIlNormale(unittest.TestCase):
    def test_mediana_normale_sulle_250_finestre_che_finiscono_all_ultima_seduta(self):
        s = series()
        b = es.reaction_blocks(s, [giorno(s, 300)], W)
        p = s.to_numpy()
        for h in W:
            self.assertAlmostEqual(b["normal_median"][h], float(np.median(es.baseline(p, len(p), h, 250))))

    def test_storia_troppo_corta_niente_mediana_normale(self):
        s = series(200)
        b = es.reaction_blocks(s, [giorno(s, 100)], W)
        self.assertEqual(b["normal_median"], {h: None for h in W})

    def test_n_effettivo_conta_una_volta_le_finestre_sovrapposte(self):
        s = series()
        b = es.reaction_blocks(s, [giorno(s, i) for i in (300, 302, 310)], W)
        self.assertEqual(b["n_eff"], {1: 3, 3: 2, 5: 2, 10: 1})


def db_con(s: pd.Series) -> str:
    path = tempfile.NamedTemporaryFile(suffix=".db", delete=False).name
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE prices (ticker TEXT, date TEXT, close REAL, adj_close REAL)")
    conn.executemany("INSERT INTO prices VALUES ('AAA', ?, ?, ?)",
                     [(d.date().isoformat(), float(v), float(v)) for d, v in s.items()])
    conn.commit()
    conn.close()
    return path


class DaRigaDiComando(unittest.TestCase):
    def setUp(self):
        self.s = con_mosse({300: 2.0, 350: -1.0, 400: 4.0, 449: 3.0})
        self.eventi = [giorno(self.s, i) for i in (300, 350, 400)]
        self.as_of = giorno(self.s, 450)

    def studio(self, s, **kw):
        with patch.object(es, "DB_PATH", db_con(s)):
            return es.run_event_study(["AAA"], self.eventi, W, as_of=self.as_of, **kw)

    def test_senza_flag_il_comportamento_non_cambia(self):
        studio = self.studio(self.s)
        self.assertNotIn("reaction", studio["AAA"])
        md = es.format_markdown(studio, W, detail=False)
        self.assertIn("### Event study — `AAA`", md)
        self.assertNotIn("Reazione", md)

    def test_i_tre_blocchi_con_le_righe_di_conclusione(self):
        studio = self.studio(self.s, reaction=True, session=giorno(self.s, 449),
                             direction="pos", direction_reference="AAA")
        md = es.format_markdown(studio, W, detail=False)
        self.assertIn("### Reazione degli analoghi — `AAA` (N=3, |z| mediano ", md)
        self.assertIn("contro 0.67 di un giorno qualsiasi)", md)
        self.assertIn("| +2.00% | +0.50% | +3.00% | 2 su 3 |", md)
        self.assertIn(f"### Reazione di oggi — `AAA`, seduta {giorno(self.s, 449)}: +3.00% (z ", md)
        self.assertIn("### Seguito — `AAA` [descrittiva] — nessuna previsione sul seguito (N=3)", md)
        self.assertIn("| mediana normale |", md)
        self.assertIn("| N eff |", md)
        self.assertNotIn("### Event study", md)

    def test_verso_coerente_solo_sull_asset_di_riferimento(self):
        studio = self.studio(self.s, reaction=True, direction="pos", direction_reference="BBB")
        self.assertIsNone(studio["AAA"]["reaction"]["coherent"])

    def test_nessun_prezzo_dalla_data_di_analisi_in_poi_entra_nei_blocchi(self):
        futuro = self.s.copy()
        futuro.iloc[450:] *= 1.5
        kw = dict(reaction=True, session=giorno(self.s, 449))
        self.assertEqual(self.studio(self.s, **kw)["AAA"]["reaction"],
                         self.studio(futuro, **kw)["AAA"]["reaction"])

    def test_seduta_di_reazione_non_ancora_chiusa(self):
        studio = self.studio(self.s, reaction=True, session=self.as_of)
        self.assertTrue(studio["AAA"]["reaction"]["today"]["missing"])
        self.assertIn("non ancora disponibile", es.format_markdown(studio, W, detail=False))


if __name__ == "__main__":
    unittest.main()
