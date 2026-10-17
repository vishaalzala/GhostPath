import json
import os
import stat
import tempfile
import unittest
from pathlib import Path

from ghostpath.reports import save_report


class ReportTests(unittest.TestCase):
    def test_create_new_private_report(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "report.json"
            result = save_report({"ok": True}, path)
            self.assertTrue(result["created"])
            self.assertEqual(json.loads(path.read_text()), {"ok": True})
            if os.name != "nt":
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

    def test_do_not_overwrite_report(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "report.json"
            path.write_text("existing")
            with self.assertRaises(FileExistsError):
                save_report({"new": True}, path)
            self.assertEqual(path.read_text(), "existing")

    def test_reject_other_extensions(self):
        with self.assertRaises(ValueError):
            save_report({"ok": True}, Path("report.txt"))
