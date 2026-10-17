import unittest

from ghostpath.presentation import ORIGINS, present


class PresentationTests(unittest.TestCase):
    def test_dashboard_cards_and_provenance(self):
        result = present("Dashboard", {
            "networkmanager": {"ready": True, "device_count": 2},
            "tor": {"installed_binary": False},
            "privoxy": {"installed_binary": False},
            "nyx": {"installed_binary": False},
            "network_modified": False,
        })
        self.assertEqual(result["provenance"], "Live local diagnostic")
        self.assertGreaterEqual(len(result["cards"]), 4)
        self.assertIn("Tor", result["caution"])
        self.assertFalse(result["technical"]["network_modified"])

    def test_privacy_cannot_claim_protection(self):
        view = present("Privacy", {
            "socks5": {"responsive": True},
            "dns": {"resolver_count": 1, "manager": "other", "leak_tested": False},
            "ipv6": {"enabled": True},
            "system_protected": False,
        })
        text = " ".join(row["value"] for row in view["cards"])
        self.assertIn("Not verified", text)
        self.assertIn("not been verified", view["caution"])

    def test_mac_preview_is_marked_as_not_applied(self):
        result = present("MAC Privacy", {"profile": "random", "applied": False})
        self.assertEqual(result["provenance_key"], "local")
        self.assertTrue(any(x["label"] == "Applied" and x["value"] == "No" for x in result["cards"]))

    def test_zero_wifi_has_explanation(self):
        result = present("Wi-Fi Audit", {
            "network_count": 0, "findings": [],
            "pmf_verified": False, "wps_verified": False,
        })
        self.assertIn("virtual Ethernet", result["summary"])
        self.assertEqual(result["findings"], [])

    def test_router_import_not_mislabelled_as_live(self):
        result = present("Router JSON", {
            "finding_count": 1,
            "findings": [
                {"code": "wps_enabled", "recommendation": "Turn off WPS", "severity": "medium"}
            ],
        })
        self.assertEqual(result["provenance"], "Offline imported evidence")
        self.assertEqual(result["findings"][0]["severity"], "medium")

    def test_suricata_and_zeek_are_imported(self):
        for title in ("Suricata EVE", "Zeek JSON"):
            with self.subTest(title=title):
                self.assertEqual(present(title, {})["provenance_key"], "imported")

    def test_ddos_training_is_not_confirmed_incident(self):
        result = present("DDoS Defence", {
            "alert_count": 4, "row_count": 24,
            "alert_threshold": 324, "alerts": [
                {"minute": 16, "reason": "Volume exceeds training threshold"},
            ],
        })
        self.assertEqual(result["provenance"], "Educational simulation")
        self.assertIn("not evidence", result["caution"])

    def test_rejects_non_mapping(self):
        with self.assertRaises(ValueError):
            present("Dashboard", "unexpected")

    def test_all_gui_sections_have_sources(self):
        names = [
            "Dashboard", "Privacy", "MAC Privacy", "Wi-Fi Audit",
            "DDoS Defence", "Learning Labs", "Router JSON",
            "Suricata EVE", "Zeek JSON", "Learning", "Reports",
        ]
        self.assertTrue(all(x in ORIGINS for x in names))
