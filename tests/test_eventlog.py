import json
import tempfile
import unittest
from pathlib import Path

from ghostpath.eventlog import analyze_event_file


class EventLogTests(unittest.TestCase):
    def test_eve_is_redacted_and_offline(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "events.jsonl")
            path.write_text(
                json.dumps({"timestamp": "2026-10-17T08:00:00+00:00", "event_type": "flow",
                            "src_ip": "192.0.2.7", "flow": {"bytes_toserver": 200,
                            "bytes_toclient": 100}}) + "\n" +
                json.dumps({"timestamp": "2026-10-17T08:01:00Z", "event_type": "alert",
                            "src_ip": "192.0.2.7"}) + "\n")
            result = analyze_event_file(path)
            self.assertEqual(result["format"], "eve")
            self.assertEqual(result["event_count"], 2)
            self.assertEqual(result["signature_alert_events"], 1)
            self.assertFalse(result["network_sent"])
            self.assertFalse(result["confirmed_ddos"])
            self.assertNotIn("192.0.2.7", json.dumps(result))
            self.assertEqual(result["per_minute"][0]["bytes"], 300)

    def test_zeek_json(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "zeek.log")
            path.write_text(json.dumps({"ts": 1792224000.0, "id.orig_h": "198.51.100.8",
                                        "proto": "udp", "orig_bytes": 60, "resp_bytes": 10}) + "\n")
            result = analyze_event_file(path, "zeek")
            self.assertEqual(result["format"], "zeek")
            self.assertEqual(result["per_minute"][0]["bytes"], 70)
            self.assertNotIn("198.51.100.8", json.dumps(result))

    def test_invalid_and_mixed_records(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "mixed.jsonl")
            path.write_text('{"timestamp":"2026-10-17T08:00:00Z","event_type":"flow"}\n'
                            '{"ts":1792224000.0,"proto":"tcp"}\n')
            with self.assertRaises(ValueError):
                analyze_event_file(path)
            path.write_text("{not valid json\n")
            with self.assertRaises(ValueError):
                analyze_event_file(path)

    def test_limits(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "large.jsonl")
            path.write_bytes(b"x" * (8 * 1024 * 1024 + 1))
            with self.assertRaises(ValueError):
                analyze_event_file(path)
            with self.assertRaises(ValueError):
                analyze_event_file(path, "untrusted")

    def test_cli(self):
        from contextlib import redirect_stdout
        from io import StringIO
        from ghostpath.cli import main
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "eve.jsonl")
            path.write_text('{"timestamp":"2026-10-17T08:00:00Z","event_type":"flow"}\n')
            output = StringIO()
            with redirect_stdout(output):
                rc = main(["defense", "events", "--file", str(path), "--format", "eve", "--json"])
            self.assertEqual(rc, 0)
            self.assertEqual(json.loads(output.getvalue())["event_count"], 1)
