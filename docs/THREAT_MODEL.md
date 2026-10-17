# GhostPath v2 — Threat model and safe operating boundaries

**Status:** Internal review draft. Independent security review remains a
requirement before claiming production readiness.

## Assets
User network configurations, application privileges, local diagnostics,
identifiers in wireless data, authorised captures and event logs.

## Trust boundaries
1. Unprivileged Python CLI/UI: user paths and text are untrusted.
2. Operating-system commands: strict read-only subprocess allowlist,
   argument validation and bounded execution time.
3. Imported PCAP, CSV and JSONL logs: potentially hostile structured
   data with maximum sizes and defensive parsing.
4. Optional Qt desktop: no root GUI or implicit network mutation.
5. GitHub/build tooling: source, dependency and release provenance.

## Threats and mitigations
- False privacy assurance: a Tor listener and local DNS settings are
  *not* evidence of network anonymity.
- Unintended network outage: no v2 firewall, DNS, routing or MAC writes.
  Future capabilities require rollback testing before activation.
- Traffic disruption: no packet injection, password attacks,
  wireless disconnections or DDoS traffic generators.
- Sensitive data leakage: reports exclude raw IPs and Wi-Fi identifiers;
  user must still redact terminal output and authorise any log sharing.
- Malformed files: enforce bounded size, line length and record counts.
- Misleading alerts: event anomalies require manual review and are
  never presented as a confirmed DDoS incident.
- Overprivileged UI: GUI must refuse to run as root.
- Supply-chain uncertainty: preserve legacy attribution and confirm
  license rights before stable distribution.

## Security acceptance criteria
- Malformed inputs cause clear errors and no network mutation.
- Offline lab and import features create no external traffic.
- Imported-event reports never include raw source IP addresses.
- Read-only diagnostics work with an ordinary user account.
- Real Kali/Parrot/Debian smoke tests precede stable support claims.
- Write-capable future builds require interruption/reboot/rollback tests.

## Scope
Analysis is limited to authorised, owned, or provided offline datasets.
The project excludes unauthorised access and disruption.
