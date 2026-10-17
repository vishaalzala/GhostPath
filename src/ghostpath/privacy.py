"""Read-only Tor SOCKS and DNS diagnostics; no traffic anonymisation claims."""
from __future__ import annotations

import ipaddress
import socket
from pathlib import Path

from .services import tor_status, proxy_status


def dns_status(path: Path = Path("/etc/resolv.conf")) -> dict[str, object]:
    """Inspect current resolver configuration without exposing resolver addresses."""
    try:
        resolved = path.resolve(strict=True)
        data = path.read_text(encoding="utf-8", errors="replace")[:16384]
    except (OSError, RuntimeError):
        return {
            "available": False, "resolver_count": 0, "local_resolver": False,
            "manager": "unknown", "leak_tested": False,
            "warning": "Resolver information unavailable; DNS leaks have not been tested.",
        }
    addresses = []
    for line in data.splitlines():
        fields = line.strip().split()
        if len(fields) > 1 and fields[0] == "nameserver":
            try:
                addresses.append(ipaddress.ip_address(fields[1]))
            except ValueError:
                continue
    target = str(resolved)
    manager = ("systemd-resolved" if "systemd/resolve" in target else
               "NetworkManager" if "NetworkManager" in target else "other")
    return {
        "available": True, "resolver_count": len(addresses),
        "local_resolver": any(addr.is_loopback for addr in addresses),
        "manager": manager, "leak_tested": False,
        "warning": "Local resolver settings alone cannot establish whether DNS leaks occur.",
    }


def tor_socks_status(timeout: float = 0.5) -> dict[str, object]:
    """Only test a local SOCKS5 handshake; never contact a remote destination."""
    result: dict[str, object] = {
        "endpoint": "127.0.0.1:9050",
        "responsive": False, "routes_traffic": False,
        "note": "A local SOCKS response is not proof of Tor routing or anonymity.",
    }
    try:
        with socket.create_connection(("127.0.0.1", 9050), timeout=timeout) as sock:
            sock.settimeout(timeout)
            sock.sendall(b"\x05\x01\x00")
            response = sock.recv(2)
            result["responsive"] = response == b"\x05\x00"
    except (OSError, TimeoutError):
        pass
    return result



def ipv6_inventory(
    disabled_path: Path = Path("/proc/sys/net/ipv6/conf/all/disable_ipv6"),
    interfaces_path: Path = Path("/proc/net/if_inet6"),
) -> dict[str, object]:
    """Read kernel IPv6 state; never modify interfaces or expose addresses."""
    enabled: bool | None = None
    try:
        flag = disabled_path.read_text(encoding="utf-8").strip()
        if flag in ("0", "1"):
            enabled = flag == "0"
    except OSError:
        pass
    count = 0
    try:
        for line in interfaces_path.read_text(encoding="utf-8").splitlines():
            fields = line.split()
            if len(fields) >= 6 and fields[-1] != "lo":
                count += 1
    except OSError:
        pass
    return {
        "enabled": enabled,
        "non_loopback_address_count": count,
        "leak_tested": False,
        "warning": "An IPv6 address count is not evidence of any leak or protection.",
    }


def privacy_report() -> dict[str, object]:
    return {
        "tor": tor_status(),
        "socks5": tor_socks_status(),
        "proxy": proxy_status(),
        "dns": dns_status(),
        "ipv4_leak_tested": False,
        "ipv6": ipv6_inventory(),
        "ipv6_leak_tested": False,
        "webrtc_leak_tested": False,
        "system_protected": False,
        "limitations": [
            "GhostPath does not enable transparent Tor routing.",
            "A working Tor process or SOCKS handshake is not a privacy guarantee.",
            "Live DNS, IPv4, IPv6 and WebRTC leak checks require separate consented tests.",
        ],
    }
