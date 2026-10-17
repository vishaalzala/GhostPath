import json
import tempfile
import unittest
from pathlib import Path

from ghostpath.config_audit import audit_file, audit_settings


class WifiOfflineConfigurationTests(unittest.TestCase):
    def test_never_exposes_network_name(self):
        report = audit_settings({
            "ssid": "Sensitive Home Wi-Fi",
            "security": "OPEN",
            "wps_enabled": True,
            "pmf": "disabled",
            "guest_isolation": False,
        })
        self.assertGreater(report["finding_count"], 0)
        self.assertFalse(report["any_connection_attempted"])
        self.assertNotIn("Sensitive Home Wi-Fi", str(report))

    def test_modern_configuration(self):
        report = audit_settings({
            "security": "WPA3", "wps_enabled": False,
            "pmf": "required", "guest_isolation": True,
        })
        self.assertEqual(report["finding_count"], 0)

    def test_rejects_malformed_json(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "broken.json"
            file.write_text("{broken")
            with self.assertRaises(ValueError):
                audit_file(file)

    def test_offline_file(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "router.json"
            file.write_text(json.dumps({"security": "WPA2", "wps_enabled": True}))
            self.assertGreater(audit_file(file)["finding_count"], 0)
