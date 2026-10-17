# GhostPath v2 — Release Gates

## Alpha code gate
- [x] Branch separation and documented source provenance
- [x] Python CLI, GUI source, offline security modules and user guide
- [x] MAC/Wi-Fi privacy recommendations are non-mutating
- [x] DDoS learning exercises use offline data only
- [x] Redacted reports with exclusive file creation
- [ ] Latest CI run passes after integration
- [ ] Manually smoke test all CLI commands on a clean Kali VM
- [ ] GUI launches on an ordinary Kali user's desktop

## Beta compatibility gate
- [ ] Kali/Debian supported-package and service test matrix
- [ ] Wi-Fi driver and monitor capabilities inventory
- [ ] Large/malformed PCAP, CSV and EVE input fuzz/regression tests
- [ ] GUI threading, file-selector and accessibility verification
- [ ] Security, licensing and dependency audit plus SBOM
- [ ] Verified updates, rollback and complete uninstall

## Production privacy-engine gate
- [ ] Safe, reversible system-level firewall/DNS configuration engine
- [ ] No unrelated nftables rule flushing
- [ ] Tor bootstrap, circuit, SOCKS and application-route verification
- [ ] DNS/IPv6/WebRTC leak validation, with honest limitations
- [ ] Controlled MAC randomisation with reconnect/restore safeguards
- [ ] Crash and reboot rollback demonstrated on supported test VMs
- [ ] Independent security review of privileged helper
- [ ] Signed releases, reproducible packages and public maintenance policy

**Go-live: BLOCKED.** The alpha source may be evaluated for education
but is not a supported system-wide privacy or production security product.
Even green GitHub Actions cannot substitute for real VM/hardware testing.
