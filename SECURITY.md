# Security policy

GhostPath v2 alpha is an educational, read-only Linux diagnostics project.
It is not a production anonymity tool or network attack framework.

- Run diagnostics without root privileges.
- Test only owned or explicitly authorized systems.
- No telemetry, DNS changes, firewall edits, packet injection or MAC writes
  are included in the current Python alpha.
- DDoS training uses offline data and isolated labs, never public floods.
- Wi-Fi content focuses on configuration, monitoring and offline analysis.
- Redact IP addresses, MACs, network names and credentials from bug reports.

## Vulnerability reporting
Do not publish credentials, private data or exploit details in a public
issue. Maintainers should enable private vulnerability reporting before
stable release.

## Stable release gates
Audited privilege helper, verified rollback and recovery, secure installer,
dependency review, SBOM, platform tests and independent security review.
