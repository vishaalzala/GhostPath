# GhostPath v2 Roadmap

## First milestone
- [x] Archive existing code and history in legacy-v1
- [x] Create develop-v2 Python development branch
- [x] Read-only Python CLI with JSON results
- [x] Tor, Privoxy and NetworkManager diagnostics
- [x] Current MAC inventory and cached connected-Wi-Fi summary
- [x] Initial mock-based unit tests and CI configuration
- [x] New user guide and security policy

## Phase 1 — Remaining foundation work
- [ ] CI results checked for supported Python versions
- [ ] Kali/Debian disposable-VM smoke tests
- [ ] Improve package-specific remediation and OS compatibility detection
- [ ] Privacy-safe structured diagnostics and support bundles
- [ ] Licensing/provenance review and release policy

## Phase 2 — Tor and network safety
- [ ] Tor SOCKS/control integration and independent health verification
- [ ] Privoxy compatibility and safe configuration validation
- [ ] DNS/IPv4/IPv6 diagnostic checks
- [ ] Privilege separation with narrowly scoped helper
- [ ] Network transaction journal, rollback and recovery testing

## Phase 3 — MAC and wireless posture
- [ ] NetworkManager MAC privacy profiles with restore
- [ ] WPA2/WPA3 and PMF security posture on authorized networks
- [ ] Optional passive wireless monitor adapter
- [ ] Offline capture review and educational lab analysis

## Phase 4 — DDoS defence
- [ ] Synthetic and authorized offline traffic datasets
- [ ] Alert baselines and anomalous event analysis
- [ ] Optional Suricata/Zeek import
- [ ] Isolated training exercises and egress isolation tests

## Phase 5 — GUI and release
- [ ] PySide6 desktop interface
- [ ] Local learning centre, reports, accessibility
- [ ] Debian package, tested installer, updater, clean uninstall
- [ ] Signed releases, SBOM, regression/security/rollback validation

Stable release is blocked until errors, reboot recovery, firewall and DNS
restoration, installation and upgrades pass documented tests.
