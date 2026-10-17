"""Bounded, strictly offline classic PCAP metadata inspection.

Reads no packet payload beyond header classification; never exposes
addresses, SSIDs or raw frames. No live capture or transmission.
"""
from __future__ import annotations

import struct
from collections import Counter
from pathlib import Path

MAX_PCAP_BYTES = 16 * 1024 * 1024
MAX_PACKETS = 10000
MAGIC = {
    b"\xd4\xc3\xb2\xa1": "<",
    b"\xa1\xb2\xc3\xd4": ">",
    b"\x4d\x3c\xb2\xa1": "<",
    b"\xa1\xb2\x3c\x4d": ">",
}


def inspect_pcap(path: Path) -> dict[str, object]:
    if not path.is_file() or path.stat().st_size > MAX_PCAP_BYTES:
        raise ValueError("Only existing classic PCAP files up to 16 MB are supported")
    with path.open("rb") as file:
        head = file.read(24)
        if len(head) != 24 or head[:4] not in MAGIC:
            raise ValueError("Not a supported classic PCAP header (PCAPNG not yet supported)")
        endian = MAGIC[head[:4]]
        major, minor, _, _, snaplen, linktype = struct.unpack(endian + "HHiiii", head[4:])
        if (major, minor) != (2, 4) or snaplen <= 0 or snaplen > 262144:
            raise ValueError("Unsupported PCAP version or snaplen")
        if linktype not in (1, 105, 127):
            raise ValueError("Supported datalinks: Ethernet, 802.11 and radiotap")
        counts: Counter[str] = Counter()
        total = 0
        while True:
            packet_header = file.read(16)
            if not packet_header:
                break
            if len(packet_header) != 16:
                raise ValueError("Truncated PCAP packet header")
            _, _, incl_len, orig_len = struct.unpack(endian + "IIII", packet_header)
            if incl_len > snaplen or incl_len > orig_len:
                raise ValueError("Invalid packet length")
            total += 1
            if total > MAX_PACKETS:
                raise ValueError("Packet count exceeds the 10,000-frame limit")
            sample = file.read(incl_len)
            if len(sample) != incl_len:
                raise ValueError("Truncated PCAP packet")
            if linktype == 1:
                if len(sample) < 14:
                    counts["truncated-ethernet"] += 1
                else:
                    ethertype = int.from_bytes(sample[12:14], "big")
                    counts[{0x0800: "ipv4", 0x86DD: "ipv6", 0x0806: "arp"}.get(ethertype, "other-ethernet")] += 1
            else:
                if linktype == 127:
                    if len(sample) < 4:
                        counts["truncated-radiotap"] += 1
                        continue
                    offset = int.from_bytes(sample[2:4], "little")
                else:
                    offset = 0
                if offset + 2 > len(sample):
                    counts["truncated-wifi"] += 1
                else:
                    frame_type = (sample[offset] >> 2) & 3
                    counts[{0: "management", 1: "control", 2: "data"}.get(frame_type, "reserved")] += 1
    return {
        "capture_kind": {1: "ethernet", 105: "802.11", 127: "radiotap"}[linktype],
        "packet_count": total,
        "protocol_categories": dict(counts),
        "raw_payloads_saved": False,
        "identifiers_exported": False,
        "note": "Offline metadata only. File source must be owned or authorised.",
    }
