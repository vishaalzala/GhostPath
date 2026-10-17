import unittest
from unittest.mock import patch

from ghostpath.core.runner import Result
from ghostpath.services import proxy_status, tor_status


class ServiceTests(unittest.TestCase):
    @patch("ghostpath.services.run_readonly", return_value=Result(False, None, "", "missing"))
    def test_missing_tor(self, _):
        result = tor_status()
        self.assertFalse(result["installed_binary"])
        self.assertFalse(result["service_active"])
        self.assertFalse(result["routing_verified"])

    @patch("ghostpath.services.run_readonly")
    def test_running_tor_is_not_a_protection_claim(self, run):
        def fake(args):
            if args[0] == "tor":
                return Result(True, 0, "Tor version", "")
            if args[-1] == "tor@default.service":
                return Result(True, 0, "LoadState=loaded\nActiveState=active\nSubState=running\n", "")
            return Result(True, 0, "LoadState=not-found\nActiveState=inactive\n", "")
        run.side_effect = fake
        self.assertTrue(tor_status()["service_active"])
        self.assertFalse(tor_status()["routing_verified"])

    @patch("ghostpath.services.run_readonly", return_value=Result(True, 0, "LoadState=loaded\nActiveState=active\n", ""))
    def test_proxy_is_not_verified(self, _):
        self.assertFalse(proxy_status()["proxy_verified"])
