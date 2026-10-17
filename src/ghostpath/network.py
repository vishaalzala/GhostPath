"""Passive local network inventory; no MAC writes or wireless scans."""
from __future__ import annotations

from pathlib import Path

from .core.runner import run_readonly


def interface_inventory(sys_class_net: Path = Path("/sys/class/net")) -> list[dict[str, str]]:
    if not sys_class_net.is_dir():
        return []
    result = []
    for address_file in sorted(sys_class_net.glob("*/address")):
        name = address_file.parent.name
        if name == "lo":
            continue
        try:
            address = address_file.read_text(encoding="utf-8").strip()
        except OSError:
            address = "unavailable"
        result.append({"interface": name, "current_mac": address})
    return result


def networkmanager_status() -> dict[str, object]:
    result = run_readonly(["nmcli", "-t", "-f", "DEVICE,TYPE,STATE", "device", "status"])
    return {
        "available": result.available,
        "ready": result.ok,
        "device_count": len([x for x in result.stdout.splitlines() if x.strip()]) if result.ok else 0,
        "note": "Read-only; MAC randomisation is not implemented in this alpha.",
    }


def connected_wifi() -> dict[str, object]:
    """Only display currently associated APs from an existing NM cache."""
    result = run_readonly(
        ["nmcli", "-t", "-f", "IN-USE,SSID,SECURITY,SIGNAL", "device", "wifi", "list", "--rescan", "no"]
    )
    connected = []
    if result.ok:
        for line in result.stdout.splitlines():
            if not line.startswith("*:"):
                continue
            # Escaped separators may occur in SSID; join middle columns.
            fields = line.split(":")
            if len(fields) >= 4:
                connected.append({
                    "ssid": ":".join(fields[1:-2]),
                    "security": fields[-2],
                    "signal": fields[-1],
                })
    return {
        "available": result.available,
        "connected": connected,
        "note": "Only cached connected-network details; no radio scans are initiated.",
    }
