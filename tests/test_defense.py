import tempfile
import unittest
from pathlib import Path

from ghostpath.defense import analyze, example_events, parse_csv


class DefenseTests(unittest.TestCase):
    def test_offline_surge_alerts(self):
        result = analyze(example_events("surge"))
        self.assertGreater(result["alert_count"], 0)
        self.assertFalse(result["confirmed_ddos"])
        self.assertEqual(result["row_count"], 24)

    def test_busy_is_not_automatically_attack(self):
        result = analyze(example_events("busy"))
        self.assertEqual(result["alert_count"], 0)

    def test_invalid_scenario(self):
        with self.assertRaises(ValueError):
            example_events("flood")

    def test_csv_round_trip(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "counts.csv"
            path.write_text("minute,requests,errors\n0,10,0\n1,20,1\n2,40,2\n")
            parsed = parse_csv(path)
            self.assertEqual(len(parsed), 3)
            self.assertEqual(analyze(parsed)["classification"], "no volume anomaly")

    def test_reject_large_or_invalid_csv(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "counts.csv"
            path.write_text("minute,requests,errors\n0,12,22\n")
            with self.assertRaises(ValueError):
                parse_csv(path)
            path.write_text("minute,requests,errors\n1,2,0\n0,5,0\n")
            with self.assertRaises(ValueError):
                parse_csv(path)
            path.write_bytes(b"X" * (1_000_001))
            with self.assertRaises(ValueError):
                parse_csv(path)

    def test_reject_negative_events(self):
        with self.assertRaises(ValueError):
            analyze([{"minute": n, "requests": -1, "errors": 0} for n in range(3)])
