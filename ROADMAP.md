# GhostPath v2 — Proposed Development Roadmap

Status: **Planning only**. Nothing on this page is implemented by the documentation update.

## Phase 0: Ownership and inventory (blocker)
- Confirm upstream licence and redistribution permissions.
- Audit package dependencies, distro support and permission requirements.
- Record every file and networking configuration the legacy installer can mutate.
- Establish disposable VM test images and baseline connectivity metrics.

## Phase 1: Safe operations (critical)
- Make dry-run default for installer, and require explicit confirmation for changes.
- Snapshot and restore all affected DNS, firewall, Tor and service configurations.
- Introduce safe interruption, rollback and idempotent uninstall.
- Test recovery after failed installation, crash and reboot.
- **Exit criteria:** baseline state restored and connectivity verified in repeatable VM tests.

## Phase 2: Modern networking (critical)
- Integrate maintained Tor, nftables and systemd service APIs.
- Respect NetworkManager and systemd-resolved and avoid conflicting ownership.
- Implement opt-in, reversible kill-switch behaviour.
- Detect IPv4, IPv6 and DNS routing discrepancies and explicitly document limits of WebRTC checks.
- **Exit criteria:** leak and recovery tests pass in each supported VM platform.

## Phase 3: New app (high)
- Python 3 CLI with informative status, diagnostic and rollback commands.
- PySide6 GUI without unnecessary root privileges; supported privileged helper.
- Clear health indicators; privacy-preserving local logs and export.
- **Exit criteria:** CLI and GUI show matching status; error paths recover cleanly.

## Phase 4: Optional integrations (medium)
- Review I2P and Privoxy integrations; drop Polipo.
- Optional MAC/hostname modification with explicit consent and reliable restoration.
- Add isolated training scenarios on DNS, Tor and firewall fundamentals.

## Phase 5: Release readiness (critical)
- CI with static analysis, shellcheck, Python tests, package manifest and dependency scan.
- Supported distro matrix; manual restore and uninstall validation.
- Versioned release notes and honest privacy-limitations documentation.
- **Exit criteria:** a release is not labelled ready until rollback, leak checks and clean-uninstall tests succeed.

## Not in scope
- Claims of untraceability or guaranteed anonymity.
- Access to third-party devices or networks without authorisation.
- Silent persistence, evasion or unauthorised monitoring features.
