# GhostPath v2 — Development Roadmap

## Implemented in 2.0.0a4
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
- [x] Offline Suricata EVE and Zeek JSON parsing with fixture tests
- [ ] Advanced user-facing learning content and accessibility review
- [x] User-only installation, packaging, update and uninstall CI testing
- [ ] Real device install, update and uninstall QA
- [ ] Third-party provenance and license review
- [x] Development artifact build, SBOM and provenance workflow (verify CI)
- [ ] Manual dependency and licensing audit; independent release signing approval
- [ ] Independent security review and owner sign-off

## Boundaries
No uncontrolled Wi-Fi intrusion, password interception, disconnection
or external traffic flooding is planned. Education and defensive
analysis operate on authorised local data or isolated synthetic labs.

## Release stage
2.0.0a4 = development alpha. See docs/RELEASE_CHECKLIST.md for NO-GO
status and the evidence needed before declaring GhostPath stable.


### Alpha completion versus production release

The currently supported **read-only and offline** features are implemented
and covered by automated tests. This does not mean GhostPath is finished
as a production privacy-routing product. No active MAC address changes,
system Tor tunnelling, DNS rewriting, credential attacks, disruptive
wireless operations or public-target traffic flooding are available.
A public stable release requires real hardware QA, rights clearance and
security sign-off; see docs/KALI_ACCEPTANCE.md.
