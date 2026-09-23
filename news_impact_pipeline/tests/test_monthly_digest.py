"""R12: regimi e scorecard del mensile sono selezionati per DATA DEL REPORT, non
'ultima fase/scorecard in assoluto' — altrimenti un report per un mese passato
citerebbe dati che allora non esistevano, o una fase KB futura."""
from datetime import date
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import monthly_digest as md


class MonthEndTests(unittest.TestCase):
    def test_month_end(self):
        self.assertEqual(md.month_end("2026-02"), date(2026, 2, 28))
        self.assertEqual(md.month_end("2026-12"), date(2026, 12, 31))


class PhaseCoversTests(unittest.TestCase):
    def test_intervallo_chiuso(self):
        self.assertTrue(md._phase_covers("2020-01-01 to 2021-12-31", date(2021, 6, 1)))
        self.assertFalse(md._phase_covers("2020-01-01 to 2021-12-31", date(2022, 1, 1)))

    def test_present_aperto(self):
        self.assertTrue(md._phase_covers("2025-01-01 to present", date(2099, 1, 1)))
        self.assertFalse(md._phase_covers("2025-01-01 to present", date(2024, 12, 31)))


class KbRegimesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        catalog = Path(self.tmp.name) / "catalog.yaml"
        catalog.write_text("""
entries:
  - title: "Studio test"
    primary_theme: geopolitics
    regime_phases:
      - fase_a: "2010-01-01 to 2019-12-31"
      - fase_b: "2020-01-01 to 2023-12-31"
      - fase_c: "2024-01-01 to present"
""", encoding="utf-8")
        self.p = patch.object(md, "CATALOG", catalog)
        self.p.start()

    def tearDown(self):
        self.p.stop()
        self.tmp.cleanup()

    def test_fase_per_data_non_ultima(self):
        # Un report per il 2021 deve leggere fase_b, non fase_c (che nel 2021 non
        # esisteva ancora): prima del fix era sempre l'ultima elencata.
        out = md.kb_regimes(date(2021, 6, 30))
        self.assertIn("fase_b", out[0])
        self.assertNotIn("fase_c", out[0])

    def test_fase_corrente(self):
        out = md.kb_regimes(date(2026, 1, 1))
        self.assertIn("fase_c", out[0])


class ScorecardExcerptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.sc_dir = Path(self.tmp.name)
        # settimana ISO 2026-W10 (lunedì 2026-03-02) e 2026-W40 (lunedì 2026-09-28, futura)
        (self.sc_dir / "2026-W10.md").write_text(
            "# Scorecard\n## In sintesi\nVecchia.\n\n"
            "## 5. Quali temi prevediamo meglio?\nTabella vecchia.\n\n"
            "## 5-bis. Su quali ASSET prevediamo meglio?\nAsset vecchi.\n",
            encoding="utf-8")
        (self.sc_dir / "2026-W40.md").write_text(
            "# Scorecard\n## In sintesi\nFutura.\n", encoding="utf-8")
        self.p = patch.object(md, "SCORECARD_DIR", self.sc_dir)
        self.p.start()

    def tearDown(self):
        self.p.stop()
        self.tmp.cleanup()

    def test_non_prende_scorecard_futura(self):
        name, excerpt = md.latest_scorecard_excerpt(date(2026, 3, 31))
        self.assertEqual(name, "2026-W10.md")
        self.assertIn("Vecchia", excerpt)
        self.assertIn("Asset vecchi", excerpt)

    def test_nessuna_scorecard_prima_della_prima(self):
        name, excerpt = md.latest_scorecard_excerpt(date(2026, 1, 1))
        self.assertEqual(name, "(nessuna)")


if __name__ == "__main__":
    unittest.main()
