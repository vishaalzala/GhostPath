import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ghostpath.privacy import dns_status, tor_socks_status


class FakeSocket:
    def __init__(self, response):
        self.response = response
        self.outgoing = b""
    def __enter__(self):
        return self
    def __exit__(self, *_):
        return False
    def settimeout(self, _):
        pass
    def sendall(self, data):
        self.outgoing += data
    def recv(self, n):
        return self.response[:n]


class PrivacyTests(unittest.TestCase):
    def test_resolver_output_reduces_identifiers(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "resolv.conf"
            path.write_text("nameserver 127.0.0.53\nnameserver 9.9.9.9\n")
            result = dns_status(path)
            self.assertTrue(result["local_resolver"])
            self.assertEqual(result["resolver_count"], 2)
            self.assertNotIn("9.9.9.9", str(result))
            self.assertFalse(result["leak_tested"])

    def test_missing_dns_file(self):
        self.assertFalse(dns_status(Path("/unlikely/ghostpath_missing_resolv.conf"))["available"])

    @patch("ghostpath.privacy.socket.create_connection")
    def test_socks_handshake_never_proves_anonymity(self, connector):
        sock = FakeSocket(b"\x05\x00")
        connector.return_value = sock
        result = tor_socks_status()
        self.assertTrue(result["responsive"])
        self.assertFalse(result["routes_traffic"])
        self.assertEqual(sock.outgoing, b"\x05\x01\x00")
        self.assertEqual(connector.call_args.args[0], ("127.0.0.1", 9050))

    @patch("ghostpath.privacy.socket.create_connection", side_effect=ConnectionRefusedError)
    def test_no_socks_port(self, _):
        self.assertFalse(tor_socks_status()["responsive"])
