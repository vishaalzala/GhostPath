# GhostPath v2 — Python architecture

## Trust model
An unprivileged Python CLI and optional PySide6 GUI share read-only core
modules. The project has no privileged helper in alpha and performs no
live firewall, MAC, DNS, Wi-Fi radio or packet-transmission actions.

## Modules
- cli.py — bounded commands, explicit offline files and JSON output
- core/runner.py — allowlisted diagnostic subprocesses; no shell
- services.py — Tor/Privoxy/Nyx service states
- privacy.py — local SOCKS5 greeting and resolver status, no leak claims
- mac_privacy.py — read-only NetworkManager MAC profile descriptions
- wifi_audit.py — encrypted mode review of cached connected networks
- captures.py — capped, metadata-only classic PCAP parser
- defense.py — bounded CSV traffic anomaly training
- traffic.py — cumulative Linux sysfs interface statistics
- labs.py — synthetic/offline learning exercises
- reports.py — explicit new report creation with restrictive file permissions
- release.py — stable release cannot be approved without external evidence
- gui.py — optional Qt tabs sharing backend functions; background workers

## Privacy limitations
Tor's daemon may be loaded without forwarding browser traffic. Even a
valid local SOCKS5 greeting is not proof of successful Tor routing.
DNS configuration alone does not establish absence of leaks.
Current beta has no independently validated Tor, IP, DNS, IPv6 or WebRTC
leak testing. UI never declares the system protected.

## Resource and privilege controls
No shell execution, bounded command timeouts, static subprocess allowlist,
data-capped CSV and PCAP readers, no real-world traffic generation.
Exports omit network identities. GUI refuses root.

## Future work
Optional authenticated Tor Control Protocol, NetworkManager D-Bus MAC
privacy with transaction rollback, vetted native packages, hardened
upgrades/uninstaller and tested nftables policy changes remain outside
this read-only release. See roadmap and go-live gates.
