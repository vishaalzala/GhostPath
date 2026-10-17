# GhostPath v2 — Linux Privacy & Defensive Security Toolkit

**Status: v2.0.0a2 development alpha. NOT production-ready and NOT an anonymity guarantee.**

GhostPath is a local-first Python 3 cybersecurity learning application for
Kali Linux and Debian-based environments. The current development version
provides **non-disruptive, read-only local diagnostics and offline defensive
analysis**. It does not change DNS, firewall rules, routing, MAC addresses,
Wi-Fi settings or Tor service state.

## What works in the Python v2 alpha

| Feature | What it does |
| --- | --- |
| System doctor | Local OS, Tor/Privoxy and NetworkManager status |
| Privacy | Local SOCKS/DNS information; not a live leak or anonymity test |
| MAC privacy | Show interface status and preview stable/random profiles; no changes |
| Wi-Fi posture | Review connected-network security without scanning |
| Owned-router JSON audit | Offline WPA2/WPA3/WPS/PMF/guest-isolation recommendations |
| Offline capture review | Strictly bounded classic PCAP metadata summaries |
| DDoS defence demo | Deterministic synthetic traffic-anomaly scenarios |
| Offline CSV analysis | Bounded minute/request/error event counts |
| Suricata EVE | Offline JSONL alert-category and severity summaries |
| Learning | Local security lessons and offline lab examples |
| Reports | Exclusive-created private JSON and escaped HTML exports |
| GUI | Optional PySide6 dashboard and offline analysis tabs |
| Release check | Returns incomplete stable-release requirements |

The Python rebuild and unit tests live on
[develop-v2](https://github.com/vishaalzala/GhostPath/tree/develop-v2).
The original Bash code remains frozen on
[legacy-v1](https://github.com/vishaalzala/GhostPath/tree/legacy-v1).

## Install as a non-root user

    git clone -b develop-v2 https://github.com/vishaalzala/GhostPath.git GhostPath-v2
    cd GhostPath-v2
    bash scripts/setup-dev.sh
    .venv/bin/ghostpath --version
    .venv/bin/ghostpath doctor --json

Python 3.11 or later is required. If `venv` support is missing,
install your distribution's python3-venv package. Do not use sudo pip,
or the old INSTALL.sh from the legacy branch.

## Command examples

    .venv/bin/ghostpath privacy status --json
    .venv/bin/ghostpath mac status --json
    .venv/bin/ghostpath mac profiles --json
    .venv/bin/ghostpath wifi status --json
    .venv/bin/ghostpath wifi audit --json
    .venv/bin/ghostpath wifi config --file examples/router.json --json
    .venv/bin/ghostpath defense demo --scenario surge --json
    .venv/bin/ghostpath defense analyze --file examples/traffic.csv --json
    .venv/bin/ghostpath defense eve --file examples/eve.jsonl --json
    .venv/bin/ghostpath labs list --json
    .venv/bin/ghostpath learn list --json
    .venv/bin/ghostpath report create --output ghostpath-report.json
    .venv/bin/ghostpath report html --output ghostpath-report.html
    .venv/bin/ghostpath release-check --json

## Optional GUI

    source .venv/bin/activate
    python -m pip install '.[gui]'
    ghostpath gui

PySide6 is optional and needs a graphical session. **Never launch
GhostPath GUI as root.** Its actions are diagnostic or offline only.

## Automated testing

    bash scripts/test.sh

GitHub Actions tests the CLI on Python 3.11, 3.12 and 3.13.
Real Kali/USB wireless adapter compatibility, rollback and GUI testing
still need documented human verification.

## Documentation

- [Detailed user guide](docs/USER_GUIDE.md)
- [Security model](SECURITY.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Developer guide](docs/DEVELOPMENT.md)
- [Release gates](docs/RELEASE_CHECKLIST.md)
- [Roadmap](ROADMAP.md)
- [History](CHANGELOG.md)

Only assess devices, routers or log files you own or have permission
to review. No Wi-Fi password-breaking, packet injection, public flood
generator or uncontrolled network interference is included.

## Unfinished production work

There is **no tested system-wide Tor routing engine, kill switch,
DNS leak guarantee, active MAC randomiser, verified automatic network
rollback, production installer, signed package, or independently
approved security review**. Stable release is blocked until required
platform and security tests pass.

The legacy scripts contain third-party attribution without a confirmed
redistribution license; confirm provenance before public stable release.
