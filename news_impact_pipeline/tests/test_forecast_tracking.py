"""R09: una previsione e' identificata (scenario, forecast_id), dichiara il suo uso,
e' riproducibile (prezzi e date target) e una correzione della scheda non riscrive
il track record gia' valutato. Ledger e schede in una cartella temporanea; il DB
di mercato si legge soltanto."""
import contextlib
import csv
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import forecast_tracking as ft

TABLE = """
| Stat | T+1 | T+3 |
|---|---|---|
| media | +0.10% | +0.20% |
| mediana | {m1} | {m3} |
| p25 | -1.00% | -2.00% |
| p75 | +1.00% | +2.00% |
| **N** | **12** | **12** |
"""


def card(bz="+0.50%", with_gspc_desc=True):
    parts = ["# Test\n\n**Data analisi**: 2026-01-05\n**Slug**: test-slug\n\n## Event study\n",
             "### Event study — `BZ=F` (Brent) [previsione]\n" + TABLE.format(m1=bz, m3=bz)]
    if with_gspc_desc:
        parts.append("### Event study — `^GSPC` [descrittiva]\n" + TABLE.format(m1="-0.30%", m3="-0.60%"))
    parts.append("### Event study — `^GSPC` [scenario: Pool B]\n" + TABLE.format(m1="+0.40%", m3="+0.90%"))
    parts.append("### Event study — `GC=F`\n" + TABLE.format(m1="+0.20%", m3="+0.30%"))
    return "\n".join(parts) + "\n## Provenance\n"


class ForecastTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.daily = Path(self.tmp.name)
        (self.daily / "2026-01-05").mkdir()
        self.card = self.daily / "2026-01-05" / "news_01.md"
        self.card.write_text(card(), encoding="utf-8")
        self.p = [patch.object(ft, "DAILY_DIR", self.daily),
                  patch.object(ft, "LEDGER_PATH", self.daily / "forecast_ledger.csv")]
        for p in self.p:
            p.start()

    def tearDown(self):
        for p in self.p:
            p.stop()
        self.tmp.cleanup()

    def run_quiet(self, fn):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            fn()
        return out.getvalue()

    def by_id(self):
        return {r["forecast_id"]: r for r in ft.load_ledger()}

    def test_dichiarazione_e_scenario(self):
        e = {(x["asset"], x["scenario"], x["horizon"]): x for x in ft.parse_card(self.card)}
        self.assertEqual(e[("BZ=F", "base", 1)]["uso"], "previsione")
        self.assertEqual(e[("^GSPC", "base", 1)]["uso"], "descrittiva")
        self.assertEqual(e[("^GSPC", "pool-b", 1)]["uso"], "scenario")
        self.assertEqual(e[("GC=F", "base", 1)]["uso"], "")          # non dichiarata
        # Mediane opposte sullo stesso asset/orizzonte: due previsioni, non una.
        self.run_quiet(ft.cmd_backfill)
        ids = self.by_id()
        self.assertEqual(float(ids["2026-01-05/test-slug/^GSPC/base/T+1"]["expected_median"]), -0.30)
        self.assertEqual(float(ids["2026-01-05/test-slug/^GSPC/pool-b/T+1"]["expected_median"]), 0.40)
        self.assertEqual(len(ids), 8)

    def test_ledger_pre_r09_non_si_duplica_ne_cambia(self):
        old = ["made_date", "slug", "card_path", "asset", "horizon", "expected_median",
               "realized_return"]
        with ft.LEDGER_PATH.open("w", newline="") as fp:
            w = csv.writer(fp)
            w.writerow(old)
            w.writerow(["2026-01-05", "test-slug", "2026-01-05/news_01.md", "GC=F", "1",
                        "9.99", "1.2345"])
        self.run_quiet(ft.cmd_backfill)
        r = self.by_id()["2026-01-05/test-slug/GC=F/base/T+1"]
        self.assertEqual((r["expected_median"], r["realized_return"]), ("9.99", "1.2345"))
        self.assertEqual(len(self.by_id()), 8)

    def test_correzione_congela_anche_pendenti(self):
        self.run_quiet(ft.cmd_backfill)
        rows = ft.load_ledger()
        for r in rows:   # T+1 di BZ=F gia' valutata
            if r["forecast_id"].endswith("BZ=F/base/T+1"):
                r["realized_return"] = "-2.0000"
        ft.write_ledger(rows)
        self.card.write_text(card(bz="-0.90%", with_gspc_desc=False), encoding="utf-8")
        out = self.run_quiet(ft.cmd_backfill)
        ids = self.by_id()
        frozen = ids["2026-01-05/test-slug/BZ=F/base/T+1"]
        self.assertEqual(float(frozen["expected_median"]), 0.50)     # track record intatto
        self.assertTrue(frozen["revised_at"])
        self.assertEqual(ids["2026-01-05/test-slug/^GSPC/base/T+3"]["uso"], "descrittiva")
        self.assertEqual(float(ids["2026-01-05/test-slug/BZ=F/base/T+3"]["expected_median"]), 0.50)   # pendente: aggiornata
        self.assertEqual(float(ids["2026-01-05/test-slug/BZ=F/base/T+1"]["expected_median"]), 0.50)
        self.assertIn("lasciate congelate", out)
        # Rilanciare non cambia nulla: idempotente.
        before = ft.LEDGER_PATH.read_text()
        self.run_quiet(ft.cmd_backfill)
        self.assertEqual(before, ft.LEDGER_PATH.read_text())

    def test_correzione_ambigua_non_mette_in_quarantena_il_registrato(self):
        self.run_quiet(ft.cmd_backfill)
        # Mediana fuori da p25-p75: la revisione è ambigua, la versione registrata no.
        self.card.write_text(card(bz="+5.00%"), encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()):
            self.run_quiet(ft.cmd_backfill)
        rows = [r for r in ft.load_ledger() if r["asset"] == "BZ=F"]
        self.assertTrue(rows)
        self.assertEqual({r["ingestion_status"] for r in rows}, {"ok"})
        self.assertEqual({float(r["expected_median"]) for r in rows}, {0.50})

    def test_evaluate_salva_ancora_e_target_e_recheck_torna(self):
        self.run_quiet(ft.cmd_backfill)
        self.run_quiet(ft.cmd_evaluate)
        r = self.by_id()["2026-01-05/test-slug/BZ=F/base/T+3"]
        self.assertTrue(r["anchor_date"] and r["target_date"] > r["anchor_date"])
        ret = (float(r["target_price"]) / float(r["anchor_price"]) - 1) * 100
        self.assertAlmostEqual(ret, float(r["realized_return"]), places=2)
        self.assertIn("0 differiscono", self.run_quiet(ft.cmd_recheck))


if __name__ == "__main__":
    unittest.main()
