"""Read-only NetworkManager privacy planning on an owned computer.

Actual MAC changes are intentionally unsupported pending rollback tests.
"""
from __future__ import annotations

from .network import interface_inventory, networkmanager_status

PROFILES = {
    "preserve": {
        "description": "Keep interface addressing unchanged.",
        "networkmanager_mode": "permanent",
        "tradeoff": "No additional address randomisation.",
    },
    "random": {
        "description": "Request a random client address per association on supported devices.",
        "networkmanager_mode": "random",
        "tradeoff": "May interrupt connections; router or driver compatibility varies.",
    },
    "stable": {
        "description": "Request a stable pseudonymous address per configured connection.",
        "networkmanager_mode": "stable",
        "tradeoff": "A persistent identifier can still be correlated over time.",
    },
}


def plan(profile: str) -> dict[str, object]:
    if profile not in PROFILES:
        raise ValueError("Unsupported MAC privacy profile")
    return {
        "profile": profile,
        **PROFILES[profile],
        "applied": False,
        "supported_here": None,
        "requires": "NetworkManager-managed connection, supported driver and explicit local approval",
        "note": "Preview only. GhostPath cannot currently change or hide a device MAC.",
    }


def status() -> dict[str, object]:
    devices = interface_inventory()
    return {
        "interface_count": len(devices),
        "interfaces": [{"interface": d["interface"], "mac_present": True} for d in devices],
        "networkmanager": networkmanager_status(),
        "profiles": list(PROFILES),
        "can_apply": False,
        "warning": "MAC addresses remain visible on local links; privacy controls do not make devices invisible.",
    }
