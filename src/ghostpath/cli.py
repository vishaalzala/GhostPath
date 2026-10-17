"""GhostPath v2 CLI: diagnostics only in alpha."""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from . import __version__
from .diagnostics import doctor, status
from .network import connected_wifi, interface_inventory
from .services import proxy_status, tor_status


def _render(data: dict[str, Any], json_mode: bool) -> None:
    if json_mode:
        print(json.dumps(data, indent=2, sort_keys=True))
        return
    for key, value in data.items():
        print(f"{key.replace('_', ' ').title()}: {value}")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ghostpath",
        description="GhostPath v2 alpha: safe, read-only Linux privacy diagnostics.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    for command in ("doctor", "status"):
        sub = commands.add_parser(command, help="Check local service and network status")
        sub.add_argument("--json", action="store_true", help="Machine-readable JSON")

    tor = commands.add_parser("tor", help="Tor diagnostics")
    tor_sub = tor.add_subparsers(dest="action", required=True)
    tor_status_parser = tor_sub.add_parser("status", help="Show Tor service state")
    tor_status_parser.add_argument("--json", action="store_true")

    proxy = commands.add_parser("proxy", help="Proxy diagnostics")
    proxy_sub = proxy.add_subparsers(dest="action", required=True)
    proxy_status_parser = proxy_sub.add_parser("status", help="Show Privoxy state")
    proxy_status_parser.add_argument("--json", action="store_true")

    mac = commands.add_parser("mac", help="MAC interface inventory")
    mac_sub = mac.add_subparsers(dest="action", required=True)
    mac_status_parser = mac_sub.add_parser("status", help="Show current interface MACs")
    mac_status_parser.add_argument("--json", action="store_true")

    wifi = commands.add_parser("wifi", help="Connected Wi-Fi information")
    wifi_sub = wifi.add_subparsers(dest="action", required=True)
    wifi_status_parser = wifi_sub.add_parser("status", help="Read cached connected Wi-Fi data")
    wifi_status_parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = make_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "doctor":
            result = doctor()
        elif args.command == "status":
            result = status()
        elif args.command == "tor":
            result = tor_status()
        elif args.command == "proxy":
            result = proxy_status()
        elif args.command == "mac":
            result = {"interfaces": interface_inventory(), "changes_supported": False}
        elif args.command == "wifi":
            result = connected_wifi()
        else:
            parser.error("Unknown diagnostic")
            return 2
        _render(result, args.json)
        return 0
    except (OSError, ValueError) as exc:
        print(f"Diagnostic failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
