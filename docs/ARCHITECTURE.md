# GhostPath v2 Architecture

## Unprivileged defensive core

The Python 3 CLI and optional PySide6 GUI share these modules:

- services.py and privacy.py — systemd service, local SOCKS and resolver status
- network.py, mac_privacy.py and wifi_audit.py — read-only interfaces and Wi-Fi posture
- config_audit.py — offline owned-router WPA/WPS/PMF configuration review
- captures.py — bounded classic PCAP metadata review without payload export
- defense.py and traffic.py — offline traffic anomaly analysis and local counters
- eve.py — offline Suricata EVE JSONL severity/category aggregation
- labs.py and lessons.py — deterministic offline education
- reports.py and html_reports.py — private local JSON and escaped HTML exports
- release.py — release blockers and evidence requirements
- core/runner.py — narrowly allowlisted read-only subprocess calls

No remote-target selection, flood generator, interference, password
retrieval or packet injection is implemented. GUI runs unprivileged.
Classic PCAP import does not provide a live capture interface.

## Privacy claims

A running Tor service or local SOCKS listener does not prove anonymity.
No transparent routing, system-wide firewall change, DNS replacement or
automatic kill switch is provided. DNS settings inspection is not a
leak test. Read docs/RELEASE_CHECKLIST.md for unimplemented gate items.

## Data and resource boundaries

- Router config assessment: local JSON <=256 KB.
- Suricata JSONL: local file <=8 MB, maximum 50,000 lines.
- Existing defensive CSV import: <=1 MB, maximum 2,000 rows.
- Classic PCAP: <=16 MB, <=10,000 packets; no payload output.
- Reports: exclusive file creation with 0600 permissions; review before sharing.
- No automatic telemetry or outbound API requests.

## Future production system-control design

Any future privileged helper must be separately reviewed and include
capability separation, immutable policy validation, network snapshots,
transaction logs, process-crash handling, reboot recovery, automated
VM fault testing and complete uninstall. Do not grant the entire GUI
root privileges or flush unrelated firewall rules.

## Licensing

The old shell scripts are archived on legacy-v1 with source attribution.
Original redistribution rights are unverified and must be resolved before
stable public packaging.
