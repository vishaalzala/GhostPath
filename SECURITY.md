# GhostPath Security Policy

GhostPath v2 is an **educational development alpha**, not a guaranteed
anonymity or production security product. Its Python version uses local
diagnostics and bounded, offline defensive analysis by design.

## Scope of approved usage

- Work on devices/networks you own or are explicitly authorised to assess.
- Do not use GhostPath for credential theft, Wi-Fi interruption, network
  floods, unauthorised access or third-party service disruption.
- Do not run the GUI or setup script as root.
- No automatic firewall, DNS, MAC, Tor service, routing or Wi-Fi changes
  are implemented in the current Python version.
- Offline imports may include sensitive information; only aggregate
  the required fields and do not publish the original captures.
- JSON/HTML exports use private permissions, but automatic redaction
  cannot guarantee removal of arbitrary sensitive content.

## Reporting a security problem

Do not disclose private vulnerabilities, credentials or personal records
in public issues. The maintainer should enable GitHub private
vulnerability reporting and publish a verified contact before release.

## Mandatory stable release controls

Independent security assessment, original code-license provenance review,
SBOM and dependency review, Kali/Debian compatibility testing, accessible
GUI QA, package signing and reproducible builds, safe upgrade/uninstall,
and recovery tests for any future system modifications.

Until these pass, stable release is blocked. See the release checklist.
