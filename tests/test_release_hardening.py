"""Safety and regressions for the read-only v2 release candidate."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ghostpath.core.runner import Result
from ghostpath.privacy import ipv6_inventory
from ghostpath.release import readiness
from ghostpath.services import tor_status


class ReleaseHardeningTests(unittest.TestCase):
    def test_ipv6_inventory_reads_without_exposing_addresses(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            disabled = root / "disabled"
            addresses = root / "if_inet6"
            disabled.write_text("0\n")
            addresses.write_text(
                "00000000000000000000000000000001 01 80 10 80 lo\n"
                "20010db8000000000000000000000001 02 40 00 80 eth0\n"
            )
            result = ipv6_inventory(disabled, addresses)
            self.assertTrue(result["enabled"])
            self.assertEqual(result["non_loopback_address_count"], 1)
            self.assertFalse(result["leak_tested"])
            self.assertNotIn("20010db8", str(result))

    def test_ipv6_inventory_unavailable(self):
        result = ipv6_inventory(Path("/not/real/ghostpath/no"), Path("/not/real/ghostpath/list"))
        self.assertIsNone(result["enabled"])
        self.assertEqual(result["non_loopback_address_count"], 0)

    @patch("ghostpath.services.run_readonly")
    def test_active_exited_wrapper_is_not_a_running_tor_daemon(self, call):
        def fake(args):
            if args[0] == "tor":
                return Result(True, 0, "Tor version", "")
            if args[-1] == "tor@default.service":
                return Result(True, 0, "LoadState=loaded\nActiveState=inactive\nSubState=dead\n", "")
            return Result(True, 0, "LoadState=loaded\nActiveState=active\nSubState=exited\n", "")
        call.side_effect = fake
        result = tor_status()
        self.assertEqual(result["selected_unit"], "tor.service")
        self.assertFalse(result["service_active"])
        self.assertFalse(result["routing_verified"])

    def test_production_release_is_still_blocked(self):
        result = readiness()
        self.assertFalse(result["stable_release_approved"])
        self.assertFalse(result["network_mutation_enabled"])
