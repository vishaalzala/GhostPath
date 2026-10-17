import subprocess
import unittest
from unittest.mock import patch

from ghostpath.core.runner import run_readonly


class RunnerTests(unittest.TestCase):
    def test_blocks_mutating_and_unapproved_commands(self):
        for args in (
            ["bash", "-c", "true"],
            ["systemctl", "start", "tor.service"],
            ["nmcli", "device", "wifi", "rescan"],
        ):
            with self.subTest(args=args), self.assertRaises(ValueError):
                run_readonly(args)

    @patch("ghostpath.core.runner.subprocess.run")
    def test_boundaries(self, execute):
        execute.return_value = subprocess.CompletedProcess(
            args=["tor", "--version"], returncode=0, stdout="Tor version", stderr=""
        )
        result = run_readonly(["tor", "--version"])
        self.assertTrue(result.ok)
        self.assertFalse(execute.call_args.kwargs["shell"])
        self.assertGreater(execute.call_args.kwargs["timeout"], 0)

    @patch("ghostpath.core.runner.subprocess.run", side_effect=FileNotFoundError)
    def test_missing_binary(self, _):
        result = run_readonly(["tor", "--version"])
        self.assertFalse(result.available)

    @patch("ghostpath.core.runner.subprocess.run", side_effect=subprocess.TimeoutExpired("tor", 4))
    def test_timeout(self, _):
        self.assertEqual(run_readonly(["tor", "--version"]).stderr, "Diagnostic timed out")
