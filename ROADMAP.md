# GhostPath v2 — Development Roadmap

## Implemented in 2.0.0a2
- [x] Preserve legacy-v1 and develop-v2 branches
- [x] Python CLI, package metadata, automated tests
- [x] Local Tor, Nyx, Privoxy and NetworkManager diagnostics
- [x] Local SOCKS5 greeting verification and resolver-status report
- [x] MAC interface privacy summary and safe plan previews
- [x] Connected Wi-Fi encryption posture assessments
- [x] Offline Ethernet/802.11/radiotap PCAP metadata inspection
- [x] Offline DDoS-event CSV anomaly detection and synthetic scenarios
- [x] Read-only Linux interface counters
- [x] Four offline educational labs and exportable JSON reports
- [x] Optional PySide6 diagnostic GUI and non-root setup
- [x] Security policy and user/development/go-live documentation

## Must be completed before claiming stable or operational protection
- [ ] Kali Linux real VM smoke tests and PySide6 GUI validation
- [ ] Debian/Parrot compatibility matrix
- [ ] Privileged helper design with explicit consent and permissions
- [ ] NetworkManager D-Bus MAC randomisation with safe transaction/rollback
- [ ] Authenticated Tor control and verified application SOCKS routing
- [ ] Independently validated DNS and IP leak checks
- [ ] Reliable nftables/DNS crash and reboot restoration if system changes added
- [ ] Optional Suricata/Zeek adapter with fixture tests
- [ ] Advanced user-facing learning content and accessibility review
- [ ] Clean installation, packaging, upgrade and uninstall testing
- [ ] Third-party provenance and license review
- [ ] SBOM, signing, vulnerability disclosure, supply-chain audit
- [ ] Independent security review and owner sign-off

## Boundaries
No uncontrolled Wi-Fi intrusion, password interception, disconnection
or external traffic flooding is planned. Education and defensive
analysis operate on authorised local data or isolated synthetic labs.

## Release stage
2.0.0a2 = development alpha. See docs/RELEASE_CHECKLIST.md for NO-GO
status and the evidence needed before declaring GhostPath stable.
