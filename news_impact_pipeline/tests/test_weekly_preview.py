"""weekly_preview.py senza rete: calendario della settimana, scenari, validatore, render.
FRED, libreria episodi ed event study sono sostituiti da valori fissi."""
from datetime import date, datetime
from pathlib import Path
import json
import struct
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import analogues
import event_study
import weekly_preview as wp

DB = Path(__file__).resolve().parents[2] / "market_data" / "market_data.db"

MAP = {"us_cpi": {"label": "CPI USA", "fred_release_id": 10},
       "us_gdp": {"label": "PIL USA", "fred_release_id": 53},
       "us_pce": {"label": "PCE USA", "fred_release_id": 54},
       "boj_decision": {"label": "Decisione BoJ", "bank": "boj"}}
CB = [{"bank": "boj", "decision": date(2026, 10, 30), "reaction_session": date(2026, 10, 30),
       "time_local": "12:00 Asia/Tokyo"},
      {"bank": "snb", "decision": date(2026, 10, 29), "reaction_session": date(2026, 10, 29),
       "time_local": "09:30 Europe/Zurich"}]
FRED = {10: [date(2026, 11, 10)], 53: [date(2026, 10, 29)], 54: [date(2026, 10, 29)]}


def fake_fred(rid, start, end):
    return [d for d in FRED.get(rid, []) if start <= d <= end]


def week(monday, as_of):
    return wp.week_events(monday, as_of, fred=fake_fred, cb=CB, events_map=MAP)


class CalendarTests(unittest.TestCase):
    def test_target_week(self):
        self.assertEqual(wp.target_week(datetime(2026, 10, 18, 18, 5, tzinfo=wp.ROME)), date(2026, 10, 19))
        self.assertIsNone(wp.target_week(datetime(2026, 10, 18, 17, 0, tzinfo=wp.ROME)))
        self.assertEqual(wp.target_week(datetime(2026, 10, 20, 9, 0, tzinfo=wp.ROME)), date(2026, 10, 19))
        self.assertIsNone(wp.target_week(datetime(2026, 10, 21, 9, 0, tzinfo=wp.ROME)))

    def test_same_day_events_stay_distinct_and_ordered(self):
        ev = week(date(2026, 10, 26), date(2026, 10, 25))
        self.assertEqual([e["id"] for e in ev if e["mapped"]],
                         ["2026-10-29:us_gdp", "2026-10-29:us_pce", "2026-10-30:boj_decision"])
        # 08:30 di New York (ora legale) = 13:30 a Roma (già ora solare)
        self.assertEqual([e["time_rome"] for e in ev if e["event_type"] == "us_gdp"], ["13:30"])
        self.assertEqual(next(e for e in ev if e["event_type"] == "boj_decision")["time_rome"], "04:00")

    def test_unmapped_bank_is_explicit(self):
        snb = [e for e in week(date(2026, 10, 26), date(2026, 10, 25)) if not e["mapped"]]
        self.assertEqual([e["event_type"] for e in snb], ["snb"])

    def test_resume_drops_past_events(self):
        self.assertEqual([e["event_type"] for e in week(date(2026, 10, 26), date(2026, 10, 30))],
                         ["boj_decision"])

    def test_map_tickers_exist_in_db(self):
        tickers = {r[0] for r in sqlite3.connect(DB).execute("SELECT ticker FROM assets")}
        for name, spec in wp.load_events_map().items():
            self.assertIn(spec["reference"], tickers, name)
            self.assertLessEqual(set(spec["assets"]), tickers, name)
            self.assertIn(spec["reference"], spec["assets"], name)
            self.assertEqual(set(spec["scenarios"]), {"pos", "neg"}, name)

    def test_cb_calendar_schema(self):
        rows = wp.load_cb_calendar()
        self.assertTrue(rows)
        self.assertTrue(all(r["bank"] in {"fed", "ecb", "boj", "boe", "pboc"} for r in rows))
        self.assertTrue(all(r["reaction_session"] >= r["decision"] for r in rows))


MAP_BOJ = {"label": "Decisione BoJ", "bank": "boj", "pool": "decisioni BoJ della libreria", "theme": "monetary_policy", "subthemes": ["boj"],
           "match_all": False, "reference": "JPY=X", "assets": ["JPY=X"], "match_query": "BoJ yen",
           "scenarios": {"pos": "accomodante", "neg": "restrittiva"}}
EVENTO_BOJ = {"id": "2026-10-23:boj_decision", "event_type": "boj_decision", "label": "Decisione BoJ",
              "reaction_session": date(2026, 10, 23), "time_rome": "04:00", "mapped": True}
EVENTO_SNB = {"id": "2026-10-23:snb", "event_type": "snb", "label": "SNB",
              "reaction_session": date(2026, 10, 23), "time_rome": "09:30", "mapped": False}
SIX = ["2016-01-29", "2016-09-21", "2022-06-16", "2023-01-19", "2024-03-19", "2025-07-31"]
TWO = ["2022-12-20", "2024-07-31"]


def episodio(day, refs):
    ev = {"event_id": f"{day}:monetary_policy:japan_release", "geo": "japan_release",
          "subthemes_local": ["boj"], "directions_by_reference": refs, "sources": ["card:x"],
          "evidence": [{"source": "card:x", "subthemes_local": ["boj"], "directions_by_reference": refs}]}
    return {"date": day, "theme": "monetary_policy", "subthemes": ["boj"], "subthemes_local": ["boj"],
            "directions_by_reference": refs, "events": [ev]}


class ScenarioTests(unittest.TestCase):
    def test_status_thresholds(self):
        self.assertEqual([wp.status_for(n) for n in (0, 4, 5, 9, 10)],
                         ["insufficiente"] * 2 + ["indicativo"] * 2 + ["ok"])

    def test_scenario_pool_has_no_look_ahead(self):
        eps = [episodio("2024-05-01", {"JPY=X": ["neg"]}), episodio("2026-10-20", {"JPY=X": ["neg"]})]
        with patch.object(analogues, "_load", return_value=eps):
            dates, _ = wp.scenario_pool(MAP_BOJ, "neg", date(2026, 10, 20))
        self.assertEqual(dates, ["2024-05-01"])

    def test_scenario_stats_median_and_share(self):
        fake = {"JPY=X": {"per_event": [{"returns": {1: 1.0}}, {"returns": {1: -2.0}}, {"returns": {1: 3.0}}],
                          "stats": {1: {"median": 1.0, "N": 3}}}}
        with patch.object(event_study, "run_event_study", return_value=fake):
            s = wp.scenario_stats(["2024-05-01", "2024-07-31", "2022-12-20"], ["JPY=X"], date(2026, 10, 18))
        self.assertEqual(s["JPY=X"]["1"], {"median": 1.0, "pos_share": 2 / 3, "N": 3, "unit": "%"})

    def test_build_marks_insufficient_and_lacune(self):
        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(wp, "scenario_pool", side_effect=lambda spec, d, before: (SIX if d == "pos" else TWO, "nota")), \
                patch.object(wp, "scenario_stats", return_value={"JPY=X": {"1": {"median": 0.1, "pos_share": 0.5, "N": 6}}}), \
                patch.object(wp, "week_events", return_value=[EVENTO_BOJ, EVENTO_SNB]), \
                patch.object(wp, "load_events_map", return_value={"boj_decision": MAP_BOJ}), \
                patch.object(wp, "related_research", return_value=[]), \
                patch.object(wp, "pool_composition", side_effect=lambda th, dates: [["boj", len(dates)]]):
            out = wp.build(date(2026, 10, 18), date(2026, 10, 18), out_root=Path(tmp))
            t = json.loads((out / "tabelle.json").read_text())
            md = (out / "tabelle.md").read_text()
        boj, snb = t["events"]
        self.assertEqual(out.name, "2026-W43")
        self.assertEqual(boj["status"], "ok")
        self.assertEqual(boj["scenarios"]["pos"]["status"], "indicativo")
        self.assertEqual(boj["scenarios"]["neg"]["status"], "insufficiente")
        self.assertEqual(boj["scenarios"]["neg"]["stats"], {})
        self.assertEqual(t["lacune"], [{"event": boj["id"], "theme": "monetary_policy", "reference": "JPY=X",
                                        "direction": "neg", "N": 2}])
        self.assertEqual(snb["status"], "non_mappato")
        self.assertIn("N=6", md)
        self.assertIn("campione dal 2016-01-29 al 2025-07-31", md)
        self.assertIn("chiusura del giorno dell'evento", md)
        self.assertIn("Pool: decisioni BoJ", md)
        self.assertIn("composizione: boj 6", md)


T = {"as_of": "2026-10-18", "events": [{"id": "2026-10-30:boj_decision", "status": "ok", "scenarios": {
    "pos": {"N": 8, "dates": ["2024-03-19"], "stats": {"JPY=X": {"10": {"median": -0.734, "pos_share": 0.375, "N": 8}}}},
    "neg": {"N": 2, "dates": ["2022-12-20"], "stats": {}}}}]}
OK = ("## 2026-10-30:boj_decision\n### Commento\nCon N=8 la mediana a T+10 è −0,73% (38% positivi), dal 2022.\n"
      "### Bozza LinkedIn\nIn 8 past episodes since 2024 (N=8), measured from the close of the release day.\n"
      "Descriptive statistics, not a forecast.\n#BankOfJapan #Yen #Markets\n")


class ValidatorTests(unittest.TestCase):
    def test_accepts_table_figures_with_comma_and_sign(self):
        self.assertEqual(wp.validate(OK, T), [])

    def test_times_and_tickers_are_not_figures(self):
        tables = dict(T, events=[dict(T["events"][0], time_rome="04:00",
                                      scenarios={"pos": dict(T["events"][0]["scenarios"]["pos"],
                                                             stats={"1482.T": {}, "^N225": {}, "JPY=X": T["events"][0]["scenarios"]["pos"]["stats"]["JPY=X"]}),
                                                 "neg": T["events"][0]["scenarios"]["neg"]})])
        text = OK.replace("dal 2022.", "dal 2022, alle 04:00 di Roma, su 1482.T e ^N225.")
        self.assertEqual(wp.validate(text, tables), [])
        self.assertTrue(wp.validate(text.replace("04:00", "05:00"), tables))

    def test_rejects_invented_figure(self):
        self.assertTrue(any("2,5" in p for p in wp.validate(OK.replace("−0,73%", "−2,5%"), T)))

    def test_rejects_missing_closing_or_section(self):
        self.assertTrue(wp.validate(OK.replace("Descriptive statistics, not a forecast.", ""), T))
        self.assertTrue(wp.validate("", T))

    def test_draft_needs_english_closing_hashtags_and_sample_start(self):
        self.assertTrue(wp.validate(OK.replace("Descriptive statistics, not a forecast.", "Statistica descrittiva, non una previsione."), T))
        self.assertTrue(wp.validate(OK.replace("#BankOfJapan #Yen #Markets", "#BankOfJapan"), T))
        self.assertTrue(wp.validate(OK.replace("since 2024", "recently"), T))

    def test_rejects_unknown_event(self):
        extra = "## 2026-10-31:fed_decision\n### Commento\nx\n### Bozza LinkedIn\nN=1 " + wp.CLOSING
        self.assertTrue(wp.validate(OK + extra, T))


def build_fixture(tmp):
    week = Path(tmp) / "2026-W44"
    week.mkdir()
    tables = {"week": "2026-W44", "monday": "2026-10-26", "as_of": "2026-10-18", "lacune": [
        {"event": "2026-10-30:boj_decision", "theme": "monetary_policy", "reference": "JPY=X", "direction": "neg", "N": 2}],
        "events": [dict(T["events"][0], event_type="boj_decision", label="Decisione BoJ", reaction_session="2026-10-30", time_rome="04:00",
                        mapped=True, reference="JPY=X", research=[{"title": "Studio BoJ", "source_file": "x", "score": 9}],
                        scenarios={d: dict(s, label=d, status="ok" if d == "pos" else "insufficiente", note="")
                                   for d, s in T["events"][0]["scenarios"].items()})]}
    (week / "tabelle.json").write_text(json.dumps(tables))
    (week / "tabelle.md").write_text(wp._markdown(tables, {}))
    return week


class RenderTests(unittest.TestCase):
    def test_render_without_text_still_has_tables_and_reason(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = wp.render(build_fixture(tmp)).read_text()
        self.assertIn("Commento e bozze non disponibili", html)
        self.assertIn("<table", html)
        self.assertIn("Lacune", html)

    def test_render_uses_valid_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            week = build_fixture(tmp)
            (week / "testo.md").write_text(OK)
            html = wp.render(week).read_text()
        self.assertIn("bozza da rivedere", html)
        self.assertIn(wp.CLOSING, html.lower())
        self.assertIn("#BankOfJapan #Yen #Markets", html)   # testo semplice: niente titolo Markdown
        self.assertNotIn("Commento e bozze non disponibili", html)

    def test_calendar_warning_once_per_day(self):
        rows = [{"bank": "fed", "decision": date(2026, 12, 10), "reaction_session": date(2026, 12, 10),
                 "time_local": "14:00 America/New_York"}]
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "avvisi.txt"
            self.assertTrue(wp.calendar_warning(date(2026, 11, 1), rows, a))
            self.assertIsNone(wp.calendar_warning(date(2026, 11, 1), rows, a))
            self.assertIsNone(wp.calendar_warning(date(2026, 9, 1), rows, a))


class ReviewFixTests(unittest.TestCase):
    def test_render_shows_gap_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = wp.render(build_fixture(tmp)).read_text()
        self.assertIn("verso neg su JPY=X", html.split("Lacune", 1)[1])

    def test_status_uses_smallest_cell_n_and_cells_show_it(self):
        stats = {"JPY=X": {str(n): {"median": 0.5, "pos_share": 0.5, "N": 8} for n in wp.WINDOWS}}
        ten = SIX + ["2024-08-07", "2024-04-29", "2023-10-31", "2022-09-22"]
        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(wp, "scenario_pool", side_effect=lambda spec, d, before: (ten, "")), \
                patch.object(wp, "scenario_stats", return_value=stats), \
                patch.object(wp, "week_events", return_value=[EVENTO_BOJ]), \
                patch.object(wp, "load_events_map", return_value={"boj_decision": MAP_BOJ}), \
                patch.object(wp, "related_research", return_value=[]), \
                patch.object(wp, "pool_composition", return_value=[]):
            out = wp.build(date(2026, 10, 18), date(2026, 10, 18), out_root=Path(tmp))
            sc = json.loads((out / "tabelle.json").read_text())["events"][0]["scenarios"]["pos"]
            md = (out / "tabelle.md").read_text()
        self.assertEqual((sc["N"], sc["N_min"], sc["status"]), (10, 8, "indicativo"))
        self.assertIn("0.50% (50%, N=8)", md)

    def test_signed_figure_must_match_sign(self):
        self.assertTrue(wp.validate(OK.replace("−0,73%", "+0,73%"), T))
        self.assertEqual(wp.validate(OK.replace("−0,73%", "0,73%"), T), [])

    def test_closing_case_and_research_years(self):
        tables = dict(T, events=[dict(T["events"][0], research=[{"title": "Studio BoJ (1998–2026)"}])])
        text = OK.replace("dal 2022.", "dal 2022 (studio 1998–2026).").replace("Descriptive statistics", "descriptive statistics")
        self.assertEqual(wp.validate(text, tables), [])

    def test_calendar_warning_per_bank(self):
        rows = [{"bank": "fed", "decision": date(2027, 12, 8)}, {"bank": "pboc", "decision": date(2026, 12, 21)}]
        with tempfile.TemporaryDirectory() as tmp:
            msg = wp.calendar_warning(date(2026, 11, 1), rows, Path(tmp) / "a.txt")
        self.assertIn("pboc", msg)


class PoolHonestyTests(unittest.TestCase):
    def test_yield_tickers_in_basis_points(self):
        fake = {"^TNX": {"per_event": [{"anchor_price": 4.0, "returns": {1: 1.25}, "targets": {1: {"target_price": 4.05}}},
                                       {"anchor_price": 4.2, "returns": {1: -2.38}, "targets": {1: {"target_price": 4.1}}}],
                         "stats": {1: {"median": -0.56, "N": 2}}}}
        with patch.object(event_study, "run_event_study", return_value=fake):
            s = wp.scenario_stats(["2024-05-01", "2024-07-31"], ["^TNX"], date(2026, 10, 18))
        cell = s["^TNX"]["1"]
        self.assertEqual(cell["unit"], "bp")
        self.assertAlmostEqual(cell["median"], -2.5)      # mediana di +5 e −10 punti base
        self.assertEqual(cell["pos_share"], 0.5)
        self.assertEqual(wp._cell(cell, 2), "-2.5 bp (50%)")

    def test_pool_composition_counts_local_labels(self):
        eps = [episodio("2024-05-01", {}), episodio("2024-07-31", {}), episodio("2023-01-19", {})]
        eps[0]["subthemes_local"] = ["boj", "rate_decision"]
        with patch.object(analogues, "_load", return_value=eps):
            comp = wp.pool_composition("monetary_policy", ["2024-05-01", "2024-07-31"])
        self.assertEqual(comp, [["boj", 2], ["rate_decision", 1]])

    def test_every_event_declares_its_pool(self):
        for name, spec in wp.load_events_map().items():
            self.assertTrue(spec.get("pool"), name)


def png_size(path):
    head = Path(path).read_bytes()[:24]
    assert head[:8] == b"\x89PNG\r\n\x1a\n"
    return struct.unpack(">II", head[16:24])


class ChartTests(unittest.TestCase):
    def test_chart_fields_are_consistent(self):
        for name, spec in wp.load_events_map().items():
            self.assertTrue(spec.get("label_en"), name)
            self.assertTrue(1 <= len(spec["chart"]) <= 3, name)
            self.assertEqual(spec["chart"][0], spec["reference"], name)
            self.assertLessEqual(set(spec["chart"]), set(spec["assets"]), name)
            self.assertEqual(set(spec["chart_labels"]), {"pos", "neg"}, name)

    def test_chart_is_square_png_and_skips_thin_scenario(self):
        spec = dict(MAP_BOJ, label_en="Bank of Japan decision", chart=["JPY=X"],
                    chart_labels={"pos": "More dovish", "neg": "More hawkish"})
        event = dict(T["events"][0], label="Decisione BoJ", reaction_session="2026-10-30",
                     scenarios={"pos": dict(T["events"][0]["scenarios"]["pos"], status="indicativo", N_min=8,
                                            stats={"JPY=X": {str(n): {"median": 0.1 * n, "pos_share": 0.5, "N": 8, "unit": "%"}
                                                             for n in wp.WINDOWS}}),
                                "neg": dict(T["events"][0]["scenarios"]["neg"], status="insufficiente", N_min=2)})
        with tempfile.TemporaryDirectory() as tmp:
            out = wp.chart(event, spec, Path(tmp) / "g.png")
            self.assertEqual(png_size(out), (1200, 1200))
        self.assertIn("More hawkish: too few episodes (N=2)", wp.chart_subtitle(event, spec))
        event["scenarios"]["pos"]["N_min"] = 6
        self.assertIn("More dovish: N=8, at least 6 per point (2024–2024)", wp.chart_subtitle(event, spec))

    def test_render_embeds_chart(self):
        with tempfile.TemporaryDirectory() as tmp:
            week = build_fixture(tmp)
            (week / "grafico-boj_decision.png").write_bytes(b"\x89PNG\r\n\x1a\nfinto")
            html = wp.render(week).read_text()
        self.assertIn("data:image/png;base64,", html)


if __name__ == "__main__":
    unittest.main()
