import tempfile
import unittest
from pathlib import Path

from ghostpath.eve import summarize_eve


class OfflineSuricataTests(unittest.TestCase):
    def test_does_not_return_ip_addresses(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "eve.jsonl"
            file.write_text(
                '{"src_ip":"192.0.2.5","event_type":"alert",'
                '"alert":{"severity":2,"category":"Policy violation"}}\n'
            )
            report = summarize_eve(file)
            self.assertEqual(report["alert_count"], 1)
            self.assertNotIn("192.0.2.5", str(report))
            self.assertFalse(report["traffic_generated"])

    def test_rejects_non_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "eve.jsonl"
            file.write_text("{oops")
            with self.assertRaises(ValueError):
                summarize_eve(file)
