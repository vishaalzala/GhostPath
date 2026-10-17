# GhostPath v2 — Go-live gates and test evidence

## Current verdict: NO-GO for stable/production distribution
The Python 2.0.0a3 build is a development alpha with isolated diagnostics
and offline educational features. A green GitHub Actions run alone is not
proof of privacy protection, installation portability or correct recovery.

| Gate | Minimum evidence | State |
| --- | --- | --- |
| Python CLI and offline labs | CI on 3.11/3.12/3.13 | Passed automated CI; real lab operation still to validate |
| Real Kali VM install | Install/upgrade/smoke-test on clean release image | Pending |
| Debian and Parrot compatibility | Smoke tests in representative VMs | Pending |
| Qt GUI functional QA | Open and navigate in desktop session | Headless Qt smoke passed; real desktop/accessibility pending |
| Package integrity | Check source/wheel, signatures, SBOM | Source/wheel build passed; signing/SBOM pending |
| Third-party code rights | Historical legacy provenance and license decision | Pending |
| Threat model and vulnerability review | Independent engineer sign-off | Pending |
| Sensitive-output review | No credentials, MACs, SSIDs in exported reports | Unit tests present; manual pending |
| Network state recovery | Prove safe failure, crash, reboot and uninstall | Not applicable to read-only alpha; future features blocked |
| Hardware wireless support | Run supported driver/adaptor matrix | Pending |
| Security update process | Dependency alerts, CVE response and disclosure policy | Pending |
| End-user documentation | Accurate user guide with risk warnings | User-scoped installer guide added; manual review pending |

## Release process
1. Review scope and permissions; do not ship legacy startup scripts.
2. Complete open issues and attach independent VM test records.
3. Re-run CI, security checks, package verification and manual smoke tests.
4. If optional privileged networking features are introduced, test
   restoration on interruption, reboot and unrelated firewall rules.
5. Obtain owner approval for license, governance and published feature claims.
6. Sign packages and publish tagged prereleases first.
7. Keep support/disclosure channels and rollback instructions accessible.

## Technical exclusions at stable release until independently accepted
- No uncontrolled Wi-Fi disconnection, credential attacks or packet injection.
- No traffic floods to external targets.
- No statement that Tor's service status proves anonymity.
- No root-run desktop application.
- No auto-flushing nftables or modifying unmanaged DNS configurations.

## Test matrix template
Record OS image ID, Python version, architecture, interface driver, test
steps, expected vs actual result, reviewer, artifacts and date for every
Kali/Debian/Parrot test run. Document network rollback on failures.

## Verified automated results on 17 October 2026
- Python 3.11, 3.12, 3.13 CI builds and tests: **passed**.
- Kali-rolling and Debian-trixie disposable container smoke tests: **passed**.
- Headless Qt tab/startup smoke test: **passed**. Not equivalent to display hardware QA.
- User-only installer, update and uninstall in an isolated HOME: **passed**.
- The v2 installer does not alter firewall, Tor, DNS or MAC settings.
- Independent real Kali hardware, full desktop and licensing review: **NOT verified**.

Evidence is in the repository's GitHub Actions runs for develop-v2. Stable
release remains blocked regardless of automated test success.
