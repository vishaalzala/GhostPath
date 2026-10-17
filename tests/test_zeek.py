import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from ghostpath.cli import main
from ghostpath.zeek import summarize_zeek


class ZeekOfflineTests(unittest.TestCase):
    def test_redacts_addresses(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "conn.log")
            path.write_text(json.dumps({
                "ts": 1792224000.25, "id.orig_h": "192.0.2.42",
                "id.resp_h": "198.51.100.15", "proto": "tcp",
                "conn_state": "SF", "orig_bytes": 150, "resp_bytes": 210,
            }) + "\n")
            result = summarize_zeek(path)
            rendered = json.dumps(result)
            self.assertEqual(result["event_count"], 1)
            self.assertEqual(result["total_reported_payload_bytes"], 360)
            self.assertNotIn("192.0.2.42", rendered)
            self.assertNotIn("198.51.100.15", rendered)
            self.assertFalse(result["network_traffic_generated"])
            self.assertFalse(result["confirmed_attack"])

    def test_invalid_and_oversized_logs(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "conn.log")
            path.write_text("{broken")
            with self.assertRaises(ValueError):
                summarize_zeek(path)
            path.write_text("{}\n")
            with self.assertRaises(ValueError):
                summarize_zeek(path)
            path.write_bytes(b"x" * 8_000_001)
            with self.assertRaises(ValueError):
                summarize_zeek(path)

    def test_cli_output(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root, "conn.log")
            path.write_text(json.dumps({"ts": 1792224000.0, "proto": "udp"}) + "\n")
            output = StringIO()
            with redirect_stdout(output):
                code = main(["defense", "zeek", "--file", str(path), "--json"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.getvalue())["event_count"], 1)
