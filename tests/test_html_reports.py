import tempfile
import unittest
from pathlib import Path

from ghostpath.html_reports import save_html_report


class HtmlReportTests(unittest.TestCase):
    def test_escaped_and_nonoverwriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "audit.html"
            result = save_html_report({"warning": "<script>alert(1)</script>"}, file)
            self.assertTrue(result["created"])
            self.assertIn("&lt;script&gt;", file.read_text())
            self.assertNotIn("<script>", file.read_text())
            with self.assertRaises(FileExistsError):
                save_html_report({}, file)
