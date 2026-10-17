# GhostPath v2 — Manual QA and go-live handoff

This checklist is for release engineers. Do not mark completed without
dated evidence and a link to the exact tested commit.

## Supported scope
- Python CLI diagnostic alpha and experimental PySide6 GUI.
- Local MAC profile previews, not active hardware address changes.
- Connected Wi-Fi posture, not password recovery or disconnections.
- Offline CSV, PCAP and JSONL security event analysis only.
- Tor/Privoxy service observation, not verified traffic anonymisation.

## Kali VM manual smoke tests
- [ ] Clean Kali VM, non-root account and a saved VM snapshot.
- [ ] Clone develop-v2; run the non-root development setup.
- [ ] Verify doctor, status, privacy status and release-check outputs.
- [ ] Check Tor absent, stopped, starting and active states where
      possible; ensure no false privacy-protection claims.
- [ ] Check NetworkManager and non-NetworkManager environments.
- [ ] Verify Wi-Fi adapter absent/connected cases; no active scans.
- [ ] Check root GUI refusal and regular-user GUI navigation.
- [ ] Review screen reader, keyboard focus and scaling usability.
- [ ] Open harmless offline EVE, Zeek, CSV and PCAP sample files.
- [ ] Test oversized, malformed, empty and mixed-format inputs.
- [ ] Export a private report and verify no identifier leakage.
- [ ] Confirm firewall, DNS, routes and MAC settings are unchanged.
- [ ] Verify packaging, updates, uninstall and documentation.
- [ ] Review licenses, third-party assets, signing and SBOM.

## Evidence
Record VM image/version, kernel, NetworkManager, Tor package version,
dependency versions, checksum, branch/commit and test outcomes.
Redact MAC addresses, SSIDs, device identifiers and private IPs.

## Production release
No stable production approval until this review and an independent
security/provenance review are signed off. CI alone is insufficient.
