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

    def test_rianalisi_kb_registra_versione_rivista_accanto_all_originale(self):
        self.run_quiet(ft.cmd_backfill)
        self.card.write_text(card(bz="-0.90%"), encoding="utf-8")
        nuova = self.daily / "2026-01-05" / "news_02.md"
        nuova.write_text(card().replace("test-slug", "nuova-slug"), encoding="utf-8")
        rev = lambda: ft.cmd_backfill(revisione="rev1200")
        self.run_quiet(rev)
        ids = self.by_id()
        orig = ids["2026-01-05/test-slug/BZ=F/base/T+1"]
        self.assertEqual(float(orig["expected_median"]), 0.50)          # mattino congelato
        self.assertTrue(orig["revised_at"])
        rivista = ids["2026-01-05/test-slug/BZ=F/base@rev1200/T+1"]
        self.assertEqual(float(rivista["expected_median"]), -0.90)
        self.assertEqual(rivista["registration"], "rianalisi_kb")
        # Scheda nata dalla rianalisi: niente originale, scenario invariato.
        self.assertEqual(ids["2026-01-05/nuova-slug/BZ=F/base/T+1"]["registration"], "rianalisi_kb")
        # Idempotente: rilanciare la stessa rianalisi non aggiunge righe.
        before = ft.LEDGER_PATH.read_text()
        self.run_quiet(rev)
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

    def test_il_seguito_del_run_11_si_registra_come_descrittiva(self):
        self.card.write_text(scheda_run11(), encoding="utf-8")
        issues = []
        e = {x["horizon"]: x for x in ft.parse_card(self.card, issues=issues)}
        self.assertEqual(issues, [])
        self.assertEqual(sorted(e), [1, 3])
        self.assertEqual((e[1]["asset"], e[1]["uso"], e[1]["scenario"]), ("BZ=F", "descrittiva", "base"))
        self.assertEqual((e[1]["expected_median"], e[3]["expected_median"]), (0.5, -0.3))
        self.assertEqual((e[1]["hist_p25"], e[1]["hist_p75"], e[1]["n_analogues"]), (-1.0, 1.0, 12))

    def test_previsione_sul_seguito_rifiutata_da_audit_e_register(self):
        self.card.write_text(scheda_run11("previsione"), encoding="utf-8")
        issues = []
        self.assertEqual(ft.parse_card(self.card, issues=issues), [])
        self.assertIn("non può essere [previsione]", issues[0])
        bad = []
        out = self.run_quiet(lambda: ft.cmd_audit("2026-01-05", require_declared=True, bad=bad))
        self.assertIn("QUARANTENA", out)
        self.assertEqual(bad, [self.card])
        with contextlib.redirect_stderr(io.StringIO()):
            self.run_quiet(lambda: ft.cmd_backfill(day="2026-01-05", live=True, skip=set(bad)))
        self.assertEqual(ft.load_ledger(), [])

    def test_wilson_al_95_per_cento(self):
        lo, hi = ft._wilson(0.0, 4)
        self.assertAlmostEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 0.4899, places=3)
        lo, hi = ft._wilson(0.5, 4)
        self.assertAlmostEqual(lo, 0.150, places=3)
        self.assertAlmostEqual(hi, 0.850, places=3)
        self.assertIsNone(ft._wilson(None, 4))
        self.assertIsNone(ft._wilson(0.5, 0))
        self.assertEqual(ft._pct_ci(0.5, 4), "50% [15–85]")
        self.assertEqual(ft._pct_ci(None, 0), "n/a")

    def test_i_giorni_unici_non_sono_le_righe(self):
        riga = lambda giorno, med, real: {"expected_median": med, "realized_return": real, "anchor_date": giorno,
                                          "made_date": giorno, "hist_p25": "-1", "hist_p75": "1"}
        m = ft.metric_summary([riga("2026-01-05", "0.5", "0.4"), riga("2026-01-05", "0.6", "0.2"),
                               riga("2026-01-06", "0.5", "-2.0"), riga("2026-01-07", "0.01", "0.3")])
        self.assertEqual((m["n_hit"], m["hit_days"]), (3, 2))      # la riga piatta non è direzionale
        self.assertEqual((m["n_band"], m["band_days"]), (4, 3))

    def test_la_5_bis_porta_wilson_sui_giorni_unici(self):
        self.run_quiet(ft.cmd_backfill)
        self.run_quiet(ft.cmd_evaluate)
        with patch.object(ft, "SCORECARD_DIR", self.daily / "_scorecard"):
            self.run_quiet(ft.cmd_scorecard)
        testo = next((self.daily / "_scorecard").glob("*.md")).read_text(encoding="utf-8")
        bis = testo.split("## 5-bis.")[1].split("## 6.")[0]
        self.assertIn("intervallo di Wilson al 95%", bis)
        riga = next(l for l in bis.splitlines() if l.startswith("| BZ=F | T+1 |"))
        self.assertRegex(riga, r"\| 1 \| (0|100)% \[\d+–\d+\] \|")   # N unici = 1, poi hit-rate con intervallo


def scheda_run11(uso="descrittiva"):
    """Scheda col blocco stampato davvero da event_study.py --reaction (Run 11b)."""
    import event_study as es
    stat = lambda med: {"mean": 0.1, "median": med, "stdev": 1.0, "p25": -1.0, "p75": 1.0, "N": 12}
    dati = {"warnings": [], "per_event": [{}], "skipped_events": [],
            "stats": {1: stat(0.5), 3: stat(-0.3)},
            "reaction": {"n": 12, "r0_median": 2.0, "r0_p25": 0.5, "r0_p75": 3.0, "abs_z_median": 1.4,
                         "coherent": (9, 12), "today": None,
                         "normal_median": {1: 0.05, 3: 0.12}, "n_eff": {1: 12, 3: 9}}}
    md = es.format_markdown({"BZ=F": dati}, [1, 3], detail=False).replace("[descrittiva]", f"[{uso}]")
    return ("# Test\n\n**Data analisi**: 2026-01-05\n**Slug**: test-slug\n\n## Event study\n\n"
            + md + "\n\n## Provenance\n")


if __name__ == "__main__":
    unittest.main()
