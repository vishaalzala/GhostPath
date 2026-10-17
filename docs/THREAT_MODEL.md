# GhostPath v2 — Threat Model (Development)

## Assets
- User's existing network configuration and connectivity
- Local device identifiers and connected Wi-Fi metadata
- Import files and locally generated security reports
- Trustworthy security-status indicators

## Trust boundaries
1. The CLI/GUI is run by an unprivileged local user.
2. System tools are invoked only with fixed read-only argument sets.
3. Import CSV/PCAP data is untrusted and must be bounded/validated.
4. Tor or a SOCKS listener is not equivalent to routing verification.
5. External Python/Qt dependencies require provenance review.
6. Existing v1 shell scripts are unsafe legacy and are excluded from v2.

## Threats and current controls

| Threat | Current mitigation |
| --- | --- |
| Untrusted CLI arguments trigger shell execution | No shell and exact command allowlist |
| Imported capture consumes excessive resources | Size, row and packet limits |
| Event analysis declares every spike a DDoS | Explicit anomaly-only results |
| Private addresses appear in Wi-Fi audit output | SSID omitted from assessment reports |
| Reports overwrite unrelated files | Exclusive new-file creation, 0600 mode |
| Tor service status mislabelled as privacy | All protection assertions explicitly false |
| GUI obtains root permissions | Launch refuses uid 0 |
| Local GUI becomes unresponsive on reads | Thread-pool worker tasks |
| Misleading MAC hide claims | Profiles are preview-only, no interface mutation |

## Deferred high-impact risks
- System-wide nftables and resolver operations are NOT implemented.
- Live MAC randomization is NOT implemented.
- No unattended background daemon, auto-update service or external telemetry.
- Compatibility with Kali-specific hardware/NetworkManager versions is unverified.
- PCAP input parser is simple; fuzzing and independent review are required
  before processing untrusted large datasets in production.

## Non-goals
- Wireless credential capture or cracking
- Deauthentication or radio interference
- Flood generation and remote network disruption
- Hidden tracking, stealth persistence or surveillance

## Release-blocking validations
Perform clean VM smoke tests, desktop QA, dependency/SBOM review,
fuzz parsing, permission tests, licence audit, vulnerability disclosure setup,
and independent security review. If future privileged modules are introduced,
repeat crash/reboot, rollback, and unrelated-rule preservation tests.
