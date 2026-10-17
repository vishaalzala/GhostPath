import unittest

from ghostpath.wifi_audit import assess_security, wifi_audit


class WiFiAuditTests(unittest.TestCase):
    def test_open_network_warns(self):
        self.assertEqual(assess_security("--")["rating"], "high")

    def test_wep_warns(self):
        self.assertEqual(assess_security("WEP")["rating"], "high")

    def test_wpa3_not_certified(self):
        self.assertEqual(assess_security("WPA3")["rating"], "informational")

    def test_hides_ssid(self):
        result = wifi_audit({"connected": [{"ssid": "Private Family SSID", "security": "WPA2", "signal": "42"}]})
        self.assertEqual(result["network_count"], 1)
        self.assertNotIn("Private Family SSID", str(result))
        self.assertFalse(result["active_scans"])
        self.assertFalse(result["pmf_verified"])
