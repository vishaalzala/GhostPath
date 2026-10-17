# Developing GhostPath v2

Development is on develop-v2; legacy-v1 preserves old shell scripts.
Stable release is blocked until Kali VM and rollback/security tests pass.

## Local development
Log in as an ordinary user. In a clone of develop-v2:

    bash scripts/setup-dev.sh
    .venv/bin/ghostpath doctor --json
    bash scripts/test.sh

The setup script creates .venv locally, installs the Python package
inside it, and refuses root. It does not install system packages,
change network settings or start services.

## Engineering rules
- New system integrations are read-only unless separately approved
  with a safe transaction and rollback test design.
- No shell=True or uncontrolled executable paths.
- No uncontrolled traffic floods or wireless interference.
- Keep educational network simulations offline or isolated.
- Never include MACs, SSIDs, passwords or tokens in logs by default.

## Testing
- GitHub Actions runs unit tests on Python 3.11 through 3.13.
- Kali/Debian VM smoke tests and GUI tests are still pending.
- The alpha does not assert Tor routing, leak prevention or anonymity.
