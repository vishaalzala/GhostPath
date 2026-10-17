import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from ghostpath.cli import main, make_parser


class CliTests(unittest.TestCase):
    def test_requires_command(self):
        with self.assertRaises(SystemExit) as result:
            make_parser().parse_args([])
        self.assertEqual(result.exception.code, 2)

    @patch("ghostpath.cli.doctor")
    def test_doctor_json(self, doctor):
        doctor.return_value = {"protected": False, "tor": {"service_active": False}}
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["doctor", "--json"]), 0)
        self.assertFalse(json.loads(output.getvalue())["protected"])

    @patch("ghostpath.cli.mac_status")
    def test_mac_status_is_a_read_only_summary(self, status):
        status.return_value = {"interfaces": [], "can_apply": False}
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["mac", "status", "--json"]), 0)
        self.assertFalse(json.loads(output.getvalue())["can_apply"])

    def test_no_uncontrolled_attack_or_network_changing_commands(self):
        parser = make_parser()
        for args in (
            ["start"], ["wifi", "attack"], ["ddos", "flood"],
            ["mac", "change"], ["tor", "start"], ["firewall", "flush"],
        ):
            with self.subTest(args=args), self.assertRaises(SystemExit):
                parser.parse_args(args)
