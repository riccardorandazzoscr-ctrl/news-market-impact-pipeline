"""Offline contract and replay demo for the isolated CPI experiment."""
import contextlib
import io
import json
import sqlite3
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cpi_lab as lab


def source(available="2020-01-14T13:30:00-05:00", retrieved="2026-10-01T12:00:00+02:00"):
    return {"publisher": "Fixture only", "document_ref": "fixture://source/1",
            "available_at": available, "retrieved_at": retrieved}


def event(month="2020-01", release="2020-02-13T08:30:00-05:00", actual="0.2", consensus="0.3", event_id=None, move="0.25"):
    release_dt = datetime.fromisoformat(release)
    observed = (release_dt - timedelta(minutes=30)).isoformat()
    fed1 = (release_dt - timedelta(days=70)).isoformat()
    fed2 = (release_dt - timedelta(days=30)).isoformat()
    actual_source = source(release)
    previous_source = source((release_dt - timedelta(days=30)).isoformat())
    return {"schema_version": 1, "event_id": event_id or f"us_cpi:{month}",
            "reference_month": month, "release_at": release,
            "metric": "headline_cpi_mom_sa", "unit": "percentage_points",
            "actual_initial": {"value": actual, "unit": "percentage_points", "source": actual_source},
            "consensus": {"value": consensus, "provider": "Fixture only",
                          "metric": "headline_cpi_mom_sa", "observed_at": observed,
                          "source": source(observed)},
            "previous_as_reported": {"value": "0.1", "unit": "percentage_points", "source": previous_source},
            "fed_history_complete_through": (release_dt - timedelta(minutes=10)).isoformat(),
            "fed_moves": [{"decision_at": fed1, "change_percentage_points": "-0.25", "source": source(fed1)},
                          {"decision_at": fed2, "change_percentage_points": move, "source": source(fed2)}],
            "verification_status": "verified", "exclusion_reason": None}


def calendar(days):
    closes = {day: f"{day}T16:00:00-05:00" for day in days}
    return {"schema_version": 1, "exchange": "XNYS", "coverage_start": days[0],
            "coverage_end": days[-1], "complete": True,
            "source": source("2026-10-01T12:00:00+02:00"), "sessions": days,
            "session_closes": closes}


class CpiLabTests(unittest.TestCase):
    def test_release_month_is_not_release_date_and_facts_are_validated(self):
        record = event()
        self.assertEqual(lab.validate_events([record]), [])
        self.assertEqual(record["reference_month"], "2020-01")
        self.assertEqual(record["release_at"][:10], "2020-02-13")
        self.assertEqual(lab.surprise_band(record), "below")
        self.assertEqual(lab.fed_regime(record), "last_move_up")

    def test_invalid_consensus_metric_timezone_numbers_and_conflicting_ids_fail(self):
        bad = event(); bad["consensus"]["observed_at"] = "2020-02-13T09:00:00-05:00"
        self.assertTrue(any("consensus" in x for x in lab.validate_events([bad])))
        bad = event(); bad["consensus"]["metric"] = "core_cpi_mom_sa"
        self.assertTrue(lab.validate_events([bad]))
        bad = event(); bad["actual_initial"]["value"] = "NaN"
        self.assertTrue(lab.validate_events([bad]))
        bad = event(); bad["release_at"] = "2020-02-13T08:30:00"
        self.assertTrue(lab.validate_events([bad]))
        self.assertTrue(any("duplicate" in x.lower() for x in lab.validate_events([event(), event(consensus="0.4")])))

    def test_actual_fact_must_be_available_at_initial_release(self):
        record = event()
        record["actual_initial"]["source"]["available_at"] = "2020-02-13T08:31:00-05:00"
        self.assertTrue(any("primo rilascio" in x for x in lab.validate_events([record])))

    def test_unknown_fed_history_is_explicit_and_conditioned_method_abstains(self):
        record = event()
        record["fed_moves"] = []
        record["fed_history_status"] = "unknown"
        record["fed_history_source"] = source()
        self.assertEqual(lab.validate_events([record]), [])
        self.assertEqual(lab.fed_regime(record), "unknown")

    def test_explicit_exclusion_may_be_incomplete_but_never_enters_verified_sample(self):
        record = {"schema_version": 1, "event_id": "us_cpi:2020-01", "reference_month": "2020-01",
                  "release_at": "2020-02-13T08:30:00-05:00", "verification_status": "excluded",
                  "exclusion_reason": "consensus source not found"}
        self.assertEqual(lab.validate_events([record]), [])
        self.assertEqual(lab.verified_events([record]), [])

    def test_market_window_requires_explicit_sessions_and_every_price(self):
        days = ["2020-02-13", "2020-02-14", "2020-02-18", "2020-02-19", "2020-02-20", "2020-02-21"]
        self.assertEqual(lab.market_window(calendar(days), "2020-02-13T08:30:00-05:00", 5), days)
        bad_calendar = calendar(days); del bad_calendar["session_closes"][days[0]]
        with self.assertRaisesRegex(ValueError, "session_closes"):
            lab.validate_calendar(bad_calendar)
        with self.assertRaisesRegex(lab.DataUnavailable, "chiusura"):
            lab.market_window(calendar(days), "2020-02-13T16:01:00-05:00", 5)
        with self.assertRaisesRegex(lab.DataUnavailable, "chiusura"):
            lab.market_window(calendar(days), "2020-02-13T16:00:00-05:00", 5)
        with self.assertRaises(lab.DataUnavailable):
            lab.market_window(calendar(days[1:]), "2020-02-13T08:30:00-05:00", 5)
        prices = dict.fromkeys(days, "100")
        prices[days[2]] = None
        with self.assertRaises(lab.DataUnavailable):
            lab.window_return(prices, days, 5)

    def test_reaction_window_anchors_on_the_session_before_release(self):
        days = ["2020-02-12", "2020-02-13", "2020-02-14"]
        protocol = dict(lab.DEFAULT_PROTOCOL, anchor_offset_sessions=-1, horizon_sessions=0)
        window = lab.market_window(calendar(days), "2020-02-13T08:30:00-05:00", 0, -1)
        self.assertEqual(window, days[:2])
        self.assertEqual(lab.window_return({"2020-02-12": "100", "2020-02-13": "99"}, window, lab.window_span(protocol)), -1)
        with self.assertRaises(lab.DataUnavailable):
            lab.market_window(calendar(days[1:]), "2020-02-13T08:30:00-05:00", 0, -1)

    def test_surprise_only_pool_ignores_fed_regime(self):
        protocol = dict(lab.DEFAULT_PROTOCOL, conditioned_methods={"conditioned": ["surprise_band", "fed_regime"],
                                                                    "surprise_only": ["surprise_band"]})
        older = event("2019-12", "2020-01-14T08:30:00-05:00", "0.1", "0.3", move="-0.25")   # sotto, Fed giù
        target = event("2020-01", "2020-02-13T08:30:00-05:00", "0.2", "0.3")               # sotto, Fed su
        windows = {older["event_id"]: ["2020-01-14", "2020-01-15"]}
        pools = lab._methods_for(target, [older, target], {older["event_id"]: 1}, windows, set(), protocol)
        self.assertEqual([e["event_id"] for e in pools["surprise_only"]], [older["event_id"]])
        self.assertEqual(pools["conditioned"], [])

    def test_prior_horizon_maturing_on_cutoff_is_not_eligible(self):
        older = event("2020-01", "2020-02-01T08:30:00-05:00")
        target = event("2020-02", "2020-02-13T08:30:00-05:00")
        windows = {older["event_id"]: ["2020-02-08", "2020-02-10", "2020-02-11", "2020-02-12", "2020-02-13", "2020-02-14"]}
        pools = lab._methods_for(target, [older, target], {older["event_id"]: 1}, windows, set(), lab.DEFAULT_PROTOCOL)
        self.assertEqual(pools["reference"], [])

    def test_replay_receipt_is_self_contained_and_report_is_reproducible(self):
        sessions = ["2020-01-10", "2020-01-13", "2020-01-14", "2020-01-15", "2020-01-16", "2020-01-17",
                    "2020-02-13", "2020-02-14", "2020-02-18", "2020-02-19", "2020-02-20", "2020-02-21",
                    "2020-03-12", "2020-03-13", "2020-03-16", "2020-03-17", "2020-03-18", "2020-03-19"]
        cal = calendar(sessions)
        records = [event("2019-12", "2020-01-14T08:30:00-05:00", "0.2", "0.2", move="-0.25"),
                   event("2020-01", "2020-02-13T08:30:00-05:00", "0.2", "0.3"),
                   event("2020-02", "2020-03-12T08:30:00-04:00", "0.3", "0.3")]
        db = sqlite3.connect(":memory:")
        db.execute("create table prices(ticker text,date text,adj_close real,close real)")
        db.executemany("insert into prices values('^GSPC',?,?,?)", [(d,100+i,100+i) for i,d in enumerate(sessions)])
        protocol = lab.DEFAULT_PROTOCOL.copy()
        protocol["minimum_pool"] = 1
        protocol["evaluation_start"] = "2020-02-01"
        episode_rows = [{"date": "2020-01-14", "theme": "macro_data", "events": [{"subthemes_local": ["inflation_print"], "evidence": [{"subthemes_local": ["inflation_print"]}]}]}]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); run_dir = lab.create_replay(root / "runs", db, protocol, records, cal, episode_rows,
                                                         code_sha="test-code", input_sha="test-input")
            first = lab.render_report(run_dir)
            db.execute("update prices set adj_close=999 where ticker='^GSPC'")
            second = lab.render_report(run_dir)
            self.assertEqual(first, second)
            self.assertIn("retrospettivo", first.lower())
            self.assertIn("dati insufficienti", first.lower())
            self.assertTrue((run_dir / "input.json").exists())
            self.assertTrue((run_dir / "decisions.jsonl").exists())
            self.assertEqual({x.name for x in run_dir.iterdir()}, {"input.json", "decisions.jsonl", "meta.json"})
        db.close()


if __name__ == "__main__":
    unittest.main()
