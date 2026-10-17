import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from ghostpath.cli import main, make_parser


class CliTests(unittest.TestCase):
    @patch("ghostpath.cli.doctor")
    def test_doctor_json(self, doctor):
        doctor.return_value = {"protected": False}
        stream = io.StringIO()
        with redirect_stdout(stream):
            self.assertEqual(main(["doctor", "--json"]), 0)
        self.assertFalse(json.loads(stream.getvalue())["protected"])

    @patch("ghostpath.cli.interface_inventory", return_value=[])
    def test_mac_does_not_change_address(self, _):
        stream = io.StringIO()
        with redirect_stdout(stream):
            self.assertEqual(main(["mac", "status", "--json"]), 0)
        self.assertFalse(json.loads(stream.getvalue())["changes_supported"])

    def test_no_dangerous_commands(self):
        for args in (["start"], ["wifi", "attack"], ["ddos", "flood"], ["mac", "change"]):
            with self.subTest(args=args), self.assertRaises(SystemExit):
                make_parser().parse_args(args)
