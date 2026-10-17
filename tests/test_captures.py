import struct
import tempfile
import unittest
from pathlib import Path

from ghostpath.captures import inspect_pcap


def example_pcap(frame, linktype=1):
    header = b"\xd4\xc3\xb2\xa1" + struct.pack("<HHiiii", 2, 4, 0, 0, 65535, linktype)
    packet = struct.pack("<IIII", 0, 0, len(frame), len(frame)) + frame
    return header + packet


class CaptureTests(unittest.TestCase):
    def test_ethernet_metadata_no_payload(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.pcap"
            frame = b"\x00" * 12 + b"\x08\x00" + b"secret-payload"
            path.write_bytes(example_pcap(frame))
            result = inspect_pcap(path)
            self.assertEqual(result["protocol_categories"]["ipv4"], 1)
            self.assertNotIn("secret-payload", str(result))
            self.assertFalse(result["raw_payloads_saved"])

    def test_wifi_management_count(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "wifi.pcap"
            path.write_bytes(example_pcap(b"\x80\x00\x00\x00", 105))
            self.assertEqual(inspect_pcap(path)["protocol_categories"]["management"], 1)

    def test_invalid_headers_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.pcap"
            path.write_bytes(b"not-a-pcap")
            with self.assertRaises(ValueError):
                inspect_pcap(path)
