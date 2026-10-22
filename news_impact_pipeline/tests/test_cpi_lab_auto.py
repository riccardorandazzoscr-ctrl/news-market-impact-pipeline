"""cpi_lab_auto.py senza rete: lettura del calendario MarketWatch, variazione BLS, record
verificato o escluso. Le fonti sono sostituite da valori fissi."""
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cpi_lab
import cpi_lab_auto as auto

ROWS = """<table><tr><th></th><th>Time (ET)</th><th>Report</th><th>Period</th><th>Actual</th><th>{col}</th><th>Previous</th></tr>
<tr><td></td><td>Tuesday, Oct. 13</td></tr>
<tr><td></td><td>8:30 AM</td><td>CPI</td><td>Aug.</td><td>-</td><td>9.9%</td><td>0.1%</td></tr>
<tr><td></td><td>Wednesday, Oct. 14</td></tr>
<tr><td></td><td>8:30 AM</td><td>Core CPI, M/M%</td><td>Sep</td><td>-</td><td>0.2%</td><td>0.3%</td></tr>
<tr><td></td><td>8:30 AM</td><td>CPI</td><td>Sep</td><td>-</td><td>0.6%</td><td>0.4%</td></tr>
</table>"""

PREV = {"reference_month": "2026-08"}
NOW = datetime(2026, 10, 14, 14, 0, tzinfo=timezone.utc)
FED = [{"decision_at": "2025-12-10T14:00:00-05:00", "change_percentage_points": "-0.25",
        "source": {"publisher": "Federal Reserve", "document_ref": "x", "available_at": "2025-12-10T14:00:00-05:00",
                   "retrieved_at": None}},
       {"decision_at": "2026-09-16T14:00:00-04:00", "change_percentage_points": "0.25",
        "source": {"publisher": "Federal Reserve", "document_ref": "y", "available_at": "2026-09-16T14:00:00-04:00",
                   "retrieved_at": None}}]
IDX = {"2026-08": Decimal("334.131"), "2026-09": Decimal("336.298")}


def build(idx=IDX, consensus=("0.6", datetime(2026, 10, 12, 12, 3, 28, tzinfo=timezone.utc), "snap")):
    with patch.object(auto, "bls_indexes", return_value=(idx, max(idx))), \
            patch.object(auto, "wayback_consensus", return_value=consensus), \
            patch.object(auto, "fed_moves", return_value=[dict(m, source=dict(m["source"])) for m in FED]):
        return auto.build_record(date(2026, 10, 14), PREV, NOW)


class CalendarPageTests(unittest.TestCase):
    def test_reads_headline_cpi_of_release_day(self):
        self.assertEqual(auto.parse_calendar(ROWS.format(col="Forecast"), date(2026, 10, 14), "2026-09"), "0.6")

    def test_other_provider_column_is_refused(self):
        self.assertIsNone(auto.parse_calendar(ROWS.format(col="Median Forecast"), date(2026, 10, 14), "2026-09"))

    def test_wrong_period_is_not_read(self):
        self.assertIsNone(auto.parse_calendar(ROWS.format(col="Forecast"), date(2026, 10, 14), "2026-10"))


class RecordTests(unittest.TestCase):
    def test_bls_rounding_and_january(self):
        self.assertEqual(auto.mom_change(IDX, "2026-09"), "0.6")
        self.assertEqual(auto.mom_change({"2025-12": Decimal("100"), "2026-01": Decimal("100.05")}, "2026-01"), "0.1")

    def test_complete_record_is_verified_and_valid(self):
        rec = build()
        self.assertEqual(rec["verification_status"], "verified", rec["exclusion_reason"])
        self.assertEqual(rec["event_id"], "us_cpi:2026-09")
        self.assertEqual(cpi_lab.validate_events([rec]), [])

    def test_missing_consensus_is_excluded_with_reason(self):
        rec = build(consensus=None)
        self.assertEqual(rec["verification_status"], "excluded")
        self.assertIn("Wayback", rec["exclusion_reason"])
        self.assertEqual(cpi_lab.validate_events([rec]), [])

    def test_bls_not_updated_yet_writes_nothing(self):
        self.assertIsNone(build(idx={"2026-08": Decimal("334.131")}))


class OutageTests(unittest.TestCase):
    def test_non_json_names_the_source(self):
        with patch.object(auto, "http_get", return_value=b""):
            with self.assertRaisesRegex(ValueError, "^FRED x: risposta non JSON"):
                auto.get_json("u", "FRED x")

    def test_alert_only_after_grace(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            stamp = Path(tmp) / "ok"
            stamp.touch()
            now = datetime.fromtimestamp(stamp.stat().st_mtime, timezone.utc)
            with patch.object(auto, "LAST_OK", stamp), patch.object(auto, "log"), \
                    patch.object(auto, "run", side_effect=ValueError("giù")), \
                    patch.object(auto, "alert") as alert:
                auto.main(["run", "--now", (now + auto.OUTAGE_GRACE / 2).isoformat()])
                alert.assert_not_called()
                auto.main(["run", "--now", (now + auto.OUTAGE_GRACE * 2).isoformat()])
                alert.assert_called_once()


if __name__ == "__main__":
    unittest.main()
