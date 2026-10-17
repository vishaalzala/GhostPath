import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ghostpath.core.runner import Result
from ghostpath.network import connected_wifi, interface_inventory


class NetworkTests(unittest.TestCase):
    def test_local_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name, mac in (("eth0", "02:11:22:33:44:55"), ("lo", "00:00:00:00:00:00")):
                target = Path(tmp, name)
                target.mkdir()
                (target / "address").write_text(mac)
            self.assertEqual(interface_inventory(Path(tmp)), [
                {"interface": "eth0", "current_mac": "02:11:22:33:44:55"}
            ])

    @patch("ghostpath.network.run_readonly")
    def test_wifi_shows_associated_entry_only(self, run):
        run.return_value = Result(True, 0, " :Guest:WPA2:15\n*:Home:WPA3:84\n :Cafe:Open:62\n", "")
        self.assertEqual(connected_wifi()["connected"], [
            {"ssid": "Home", "security": "WPA3", "signal": "84"}
        ])

    @patch("ghostpath.network.run_readonly", return_value=Result(False, None, "", "missing"))
    def test_missing_nmcli(self, _):
        self.assertEqual(connected_wifi()["connected"], [])
