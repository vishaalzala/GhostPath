"""GhostPath v2 — safe local diagnostics and offline educational tools."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .captures import inspect_pcap
from .defense import analyze, example_events, parse_csv
from .eventlog import analyze_event_file
from .diagnostics import doctor, status
from .labs import list_labs, run_lab
from .mac_privacy import plan as mac_plan, status as mac_status
from .network import connected_wifi
from .privacy import privacy_report
from .release import readiness
from .reports import build_report, save_report
from .services import proxy_status, tor_status
from .traffic import counters
from .wifi_audit import wifi_audit


def _render(data: dict[str, Any], json_mode: bool) -> None:
    if json_mode:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        for key, value in data.items():
            print(f"{key.replace('_', ' ').title()}: {value}")


def _json_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON")


def _action(group: argparse.ArgumentParser, command: str) -> argparse.ArgumentParser:
    subs = group.add_subparsers(dest="action", required=True)
    return subs.add_parser(command)


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ghostpath",
        description="GhostPath v2: safe privacy diagnostics and offline cybersecurity learning.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("doctor", "status", "release-check"):
        _json_option(commands.add_parser(name))

    tor = commands.add_parser("tor", help="Read-only Tor service information")
    _json_option(_action(tor, "status"))
    proxy = commands.add_parser("proxy", help="Read-only Privoxy information")
    _json_option(_action(proxy, "status"))

    privacy = commands.add_parser("privacy", help="Local SOCKS5 and DNS diagnostics")
    _json_option(_action(privacy, "status"))

    mac = commands.add_parser("mac", help="Read-only MAC information and profile preview")
    sub = mac.add_subparsers(dest="action", required=True)
    for name in ("status", "profiles"):
        _json_option(sub.add_parser(name))
    planning = sub.add_parser("plan")
    planning.add_argument("profile", choices=["preserve", "stable", "random"])
    _json_option(planning)

    wifi = commands.add_parser("wifi", help="Non-invasive Wi-Fi security review")
    sub = wifi.add_subparsers(dest="action", required=True)
    for name in ("status", "audit"):
        _json_option(sub.add_parser(name))
    capture = sub.add_parser("capture", help="Analyse an offline, authorised classic PCAP")
    capture.add_argument("--file", required=True, type=Path)
    _json_option(capture)

    defense = commands.add_parser("defense", help="Offline DDoS defence analytics")
    sub = defense.add_subparsers(dest="action", required=True)
    example = sub.add_parser("demo", help="Analyze deterministic synthetic event counts")
    example.add_argument("--scenario", choices=["normal", "surge", "busy"], default="surge")
    _json_option(example)
    csv_parser = sub.add_parser("analyze", help="Analyze local, bounded CSV event counts")
    csv_parser.add_argument("--file", required=True, type=Path)
    _json_option(csv_parser)
    capture = sub.add_parser("capture", help="Inspect metadata of a local classic PCAP")
    capture.add_argument("--file", required=True, type=Path)
    _json_option(capture)
    offline_events = sub.add_parser("events", help="Analyse authorised offline Suricata/Zeek JSONL")
    offline_events.add_argument("--file", required=True, type=Path)
    offline_events.add_argument("--format", choices=["auto", "eve", "zeek"], default="auto")
    _json_option(offline_events)
    _json_option(sub.add_parser("counters", help="Read local sysfs interface counters"))

    labs = commands.add_parser("labs", help="Offline educational exercises")
    sub = labs.add_subparsers(dest="action", required=True)
    _json_option(sub.add_parser("list"))
    lab = sub.add_parser("run")
    lab.add_argument("name", choices=["traffic-baseline", "traffic-anomaly", "wifi-hardening", "mac-privacy"])
    _json_option(lab)

    reports = commands.add_parser("report", help="Create a private local JSON assessment")
    report_sub = reports.add_subparsers(dest="action", required=True)
    create = report_sub.add_parser("create")
    create.add_argument("--output", required=True, type=Path)
    _json_option(create)

    commands.add_parser("gui", help="Launch optional PySide6 desktop interface")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = make_parser()
    args = parser.parse_args(argv)
    if args.command == "gui":
        from .gui import main as gui_main
        return gui_main()
    try:
        if args.command == "doctor":
            result = doctor()
        elif args.command == "status":
            result = status()
        elif args.command == "release-check":
            result = readiness()
        elif args.command == "tor":
            result = tor_status()
        elif args.command == "proxy":
            result = proxy_status()
        elif args.command == "privacy":
            result = privacy_report()
        elif args.command == "mac":
            if args.action == "status":
                result = mac_status()
            elif args.action == "profiles":
                result = {"profiles": [mac_plan(n) for n in ("preserve", "stable", "random")]}
            else:
                result = mac_plan(args.profile)
        elif args.command == "wifi":
            if args.action == "status":
                result = connected_wifi()
            elif args.action == "audit":
                result = wifi_audit()
            else:
                result = inspect_pcap(args.file)
        elif args.command == "defense":
            if args.action == "demo":
                result = analyze(example_events(args.scenario))
            elif args.action == "analyze":
                result = analyze(parse_csv(args.file))
            elif args.action == "events":
                result = analyze_event_file(args.file, args.format)
            elif args.action == "capture":
                result = inspect_pcap(args.file)
            else:
                result = counters()
        elif args.command == "labs":
            result = list_labs() if args.action == "list" else run_lab(args.name)
        elif args.command == "report":
            result = save_report(build_report(), args.output)
        else:
            parser.error("Unknown command")
            return 2
        _render(result, args.json)
        return 0
    except (OSError, ValueError) as exc:
        print(f"GhostPath: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
