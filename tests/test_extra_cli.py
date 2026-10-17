import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from ghostpath.cli import main


class ExtraCliTests(unittest.TestCase):
    def test_router_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "config.json"
            file.write_text('{"security":"OPEN", "wps_enabled":true}')
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(["wifi", "config", "--file", str(file), "--json"])
            self.assertEqual(code, 0)
            self.assertFalse(json.loads(output.getvalue())["any_connection_attempted"])

    def test_offline_eve(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "eve.jsonl"
            file.write_text('{"event_type":"alert","alert":{"severity":1,"category":"Example"}}\n')
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(["defense", "eve", "--file", str(file), "--json"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.getvalue())["alert_count"], 1)

    def test_learning(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["learn", "show", "wifi", "--json"]), 0)
        self.assertTrue(json.loads(output.getvalue())["offline_only"])

    def test_html_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "assessment.html"
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["report", "html", "--output", str(file), "--json"]), 0)
            self.assertTrue(file.is_file())
