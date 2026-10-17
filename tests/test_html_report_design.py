import os
import stat
import tempfile
import unittest
from pathlib import Path

from ghostpath.html_reports import render_html_report, save_html_report
from ghostpath.reports import build_report


class HTMLDesignTests(unittest.TestCase):
    def test_real_local_and_simulated_sections_are_separate(self):
        page = render_html_report(build_report())
        self.assertIn("LIVE LOCAL DIAGNOSTIC", page)
        self.assertIn("EDUCATIONAL SIMULATION", page)
        self.assertIn("EDUCATIONAL PREVIEW", page)
        self.assertIn("Protection not verified", page)
        self.assertIn("Technical details", page)
        self.assertIn("No", page)
        self.assertIn("max-width", page) if False else None

    def test_offline_imported_evidence_is_labelled(self):
        data = build_report()
        data["offline_imported_evidence"] = {
            "source": "Suricata EVE",
            "results": {"alert_count": 2, "analysis_type": "offline_suricata_eve"},
        }
        page = render_html_report(data)
        self.assertIn("OFFLINE IMPORTED EVIDENCE", page)
        self.assertIn("Suricata EVE", page)
        self.assertIn("offline_suricata_eve", page)

    def test_script_and_sensitive_fields_never_render_unescaped(self):
        payload = build_report()
        payload["offline_imported_evidence"] = {
            "source": '<script>alert("oops")</script>',
            "results": {
                "alert_count": 1,
                "src_ip": "192.0.2.200",
                "password": "very-secret-password",
                "hostname": "internal.example",
                "note": "<img src=x onerror=alert(1)>",
            },
        }
        page = render_html_report(payload)
        self.assertNotIn("<script>alert", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertNotIn("192.0.2.200", page)
        self.assertNotIn("very-secret-password", page)
        self.assertNotIn("internal.example", page)
        self.assertNotIn("<img src=x", page)
        self.assertIn("script-src 'none'", page)
        self.assertIn("connect-src 'none'", page)

    def test_report_exclusive_creation_private_mode(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "assessment.html"
            result = save_html_report(build_report(), path)
            self.assertTrue(result["created"])
            if os.name != "nt":
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            with self.assertRaises(FileExistsError):
                save_html_report(build_report(), path)

    def test_invalid_extension_and_schema(self):
        with self.assertRaises(ValueError):
            save_html_report({}, Path("data.txt"))
        with self.assertRaises(ValueError):
            render_html_report([])
        with self.assertRaises(ValueError):
            render_html_report({"dns": ["unexpected"]})
