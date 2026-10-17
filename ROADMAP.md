# GhostPath v2 Implementation & Go-live Roadmap

## Code completed on the development branch

- [x] Python 3 CLI and optional PySide6 desktop dashboard
- [x] Tor/Privoxy and DNS status diagnostics
- [x] Read-only MAC inventory and NetworkManager privacy profile preview
- [x] Connected-Wi-Fi posture analysis
- [x] Offline WPA2/WPA3/WPS/PMF owned-router configuration assessment
- [x] Bounded classic PCAP metadata review with no payload export
- [x] Offline synthetic DDoS anomaly analysis and CSV importer
- [x] Offline Suricata EVE alert aggregation without exporting IPs
- [x] Offline educational labs and lessons
- [x] Privacy-reduced JSON and escaped HTML local reports
- [x] Non-root developer installation, unit tests and CI workflow
- [x] Legacy isolation, security policy, release checklist, user guide

## Not completed: production release blockers

- [ ] Perform clean Kali and Debian VM installation and full smoke tests
- [ ] GUI run and accessibility verification on a real Linux desktop
- [ ] Verify supported internal and external Wi-Fi hardware/driver matrix
- [ ] Complete Tor SOCKS circuit health and independent application routing checks
- [ ] Implement opt-in MAC changes only after tested rollback and driver compatibility
- [ ] Implement any system-wide firewall/DNS mutation only after recovery audits
- [ ] Demonstrate restore after crashes, power failure and reboots
- [ ] Package/sign releases, make SBOM and third-party license review
- [ ] Complete threat model, dependency audit and external code security review
- [ ] Establish supported operating systems and maintainer vulnerability channels

## Project principles

The alpha never transmits network floods, disconnects wireless clients,
attempts passwords, secretly accesses networks, or claims verified anonymity.
High-risk system changes remain disabled until hardware/rollback testing.

Read docs/RELEASE_CHECKLIST.md to decide when a stable go-live is warranted.
