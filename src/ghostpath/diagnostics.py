"""Unprivileged health inventory; never changes network settings."""
from __future__ import annotations

import os
import platform
from pathlib import Path

from . import __version__
from .network import interface_inventory, networkmanager_status
from .services import nyx_status, proxy_status, tor_status


def doctor() -> dict[str, object]:
    platform_name = platform.system()
    is_root = hasattr(os, "geteuid") and os.geteuid() == 0
    return {
        "version": __version__,
        "platform": platform_name,
        "supported_platform": platform_name == "Linux",
        "running_as_root": is_root,
        "warnings": (
            ["GhostPath v2 diagnostics do not need root privileges; run as a normal user."]
            if is_root else []
        ),
        "tor": tor_status(),
        "privoxy": proxy_status(),
        "nyx": nyx_status(),
        "networkmanager": networkmanager_status(),
        "privacy_session": "unavailable",
        "network_modified": False,
    }


def status() -> dict[str, object]:
    return {
        "version": __version__,
        "tor": tor_status(),
        "proxy": proxy_status(),
        "interfaces": interface_inventory(),
        "firewall_managed": False,
        "dns_managed": False,
        "privacy_session": "not implemented",
        "protected": False,
    }
