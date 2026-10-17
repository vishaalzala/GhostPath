# GhostPath v2 — Python Alpha

**Local-first Linux privacy and defensive cybersecurity diagnostics.**

**Status: v2.0.0a1 / development only. NOT a production privacy or anonymity tool.**

This `develop-v2` branch contains a fresh Python 3 CLI with read-only
diagnostics. It does not change DNS, routes, MAC addresses, Wi-Fi interfaces,
firewalls or Tor configurations, and does not start or stop services.

Legacy Bash scripts and their history remain in `legacy-v1`. The `main`
branch remains unchanged until v2 passes release gates.

## Test in Kali Linux or Debian

Use a normal user account and a disposable test environment.

```bash
git clone https://github.com/vishaalzala/GhostPath.git
cd GhostPath
git switch develop-v2
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --no-deps -e .
ghostpath doctor --json
```

If venv support is missing, install the system's python3-venv package using
the OS package manager. Do not run `sudo pip install`.

## Available alpha commands

```bash
ghostpath --version
ghostpath doctor
ghostpath doctor --json
ghostpath status --json
ghostpath tor status --json
ghostpath proxy status --json
ghostpath mac status --json
ghostpath wifi status --json
```

Tor, Privoxy, Nyx and NetworkManager are optional for this diagnostic alpha.
Missing packages are reported rather than automatically installed.

## Not implemented

No Tor traffic routing, firewall modifications, DNS changes, MAC spoofing,
active Wi-Fi intrusion, DDoS traffic generation, graphical interface, or
anonymity guarantees. Do not use scripts from the old branch.

## Run tests

```bash
python -m unittest discover -s tests -v
```

See [User Guide](docs/USER_GUIDE.md), [Architecture](docs/ARCHITECTURE.md),
[Security](SECURITY.md) and [Roadmap](ROADMAP.md).

## Provenance

The legacy scripts have third-party authorship and do not have a verified
redistribution license. Their attribution/history remain in `legacy-v1`.
The Python modules are newly written and do not copy those shell scripts.
License review is required before public stable distribution.
