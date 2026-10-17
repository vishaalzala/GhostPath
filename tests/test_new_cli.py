import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from ghostpath.cli import main


class NewCliTests(unittest.TestCase):
    def test_offline_defense_demo(self):
        stream = io.StringIO()
        with redirect_stdout(stream):
            self.assertEqual(main(["defense", "demo", "--scenario", "surge", "--json"]), 0)
        self.assertFalse(json.loads(stream.getvalue())["confirmed_ddos"])

    def test_release_check_blocks_stable(self):
        stream = io.StringIO()
        with redirect_stdout(stream):
            self.assertEqual(main(["release-check", "--json"]), 0)
        self.assertFalse(json.loads(stream.getvalue())["stable_release_approved"])

    def test_offline_lab(self):
        stream = io.StringIO()
        with redirect_stdout(stream):
            self.assertEqual(main(["labs", "run", "wifi-hardening", "--json"]), 0)
        self.assertTrue(json.loads(stream.getvalue())["offline_only"])

    def test_export_report(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "assessment.json"
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["report", "create", "--output", str(target), "--json"]), 0)
            self.assertTrue(target.is_file())

    @patch("ghostpath.cli.mac_status")
    def test_mac_no_live_changes(self, status):
        status.return_value = {"can_apply": False}
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["mac", "status", "--json"]), 0)
        self.assertFalse(json.loads(output.getvalue())["can_apply"])
