# GhostPath v2 — Python Security Toolkit

**Current development version: 2.0.0a2 (alpha).**
Privacy diagnostics, defensive Wi-Fi assessments and offline DDoS education.
**This is NOT a production anonymity tool, live Wi-Fi attack suite, or DDoS generator.**

GhostPath v2 is a local-first Python 3 rebuild. It does not silently change
firewall, DNS, network routing, MAC addresses or service states. All real
traffic-related capabilities are read-only; training scenarios are offline.
Running Tor is not evidence that applications use Tor.

## Features already implemented

| Module | Available today |
| --- | --- |
| Diagnostics | Tor, Privoxy, Nyx and NetworkManager presence/status |
| Privacy | Loopback-only SOCKS5 handshake check and local DNS config review |
| MAC Privacy | Interface inventory without publishing raw MACs; profile previews |
| Wi-Fi Security | Cached connected-network review and WPA2/WPA3/WEP posture guidance |
| Offline PCAP | Strict-size classic PCAP metadata parsing; no packet payload export |
| DDoS Defence | Cumulative local counters, bounded CSV anomaly analysis, synthetic scenarios |
| Learning | Four offline guided lab exercises |
| Reports | Explicitly requested new local JSON reports with private file permissions |
| Desktop | Optional PySide6 multi-tab read-only dashboard |
| Quality | Automated Python tests, CI, security policy and release criteria |

Not implemented: system-wide Tor routing, verified leak protection, active MAC
changes, real-time DDoS mitigation, wireless intrusion or disruptive traffic,
full platform compatibility, safe restore from legacy sessions. The v2 GUI
is a development interface, not a validated stable release.

## Install for Kali Linux (normal user account, NOT root)

If you previously installed the Bash version, do NOT run its old installer or
the old ghostpath-on/off commands. Work in a new folder.

\`\`\`bash
cd ~/Desktop
git clone -b develop-v2 https://github.com/vishaalzala/GhostPath.git GhostPath-v2
cd GhostPath-v2
bash scripts/setup-dev.sh
.venv/bin/ghostpath --version
.venv/bin/ghostpath doctor --json
\`\`\`

If Python venv creation fails, use the Kali package manager to install
\`python3-venv\` before rerunning setup. The installer only writes into the
project-local Python virtual environment; it does not modify network settings.

### Optional desktop interface

\`\`\`bash
source .venv/bin/activate
python -m pip install -e '.[gui]'
ghostpath gui
\`\`\`

A graphical desktop session is required. GUI dependencies are optional
because they may be large and are not needed for terminal use.

## Usage

\`\`\`bash
ghostpath doctor --json
ghostpath status --json
ghostpath privacy status --json
ghostpath tor status --json
ghostpath proxy status --json
ghostpath mac status --json
ghostpath mac profiles --json
ghostpath mac plan stable --json
ghostpath wifi audit --json
ghostpath defense counters --json
ghostpath defense demo --scenario surge --json
ghostpath defense analyze --file data.csv --json
ghostpath wifi capture --file authorized-sample.pcap --json
ghostpath labs list --json
ghostpath labs run traffic-anomaly --json
ghostpath report create --output my-report.json --json
ghostpath release-check --json
\`\`\`

For CSV input use a file with the columns \`minute,requests,errors\`.
Minutes must increase; max 2,000 rows and 1 MB. All analysis is offline.
Classic Ethernet, 802.11 and radiotap PCAPs are supported (up to 16 MB and
10,000 packets); PCAPNG is not supported.

See [User Guide](docs/USER_GUIDE.md) for examples, output interpretation,
installation troubleshooting and privacy caveats.

## Testing

\`\`\`bash
bash scripts/test.sh
\`\`\`

GitHub Actions runs unit tests across Python 3.11–3.13 and builds packages.
Passing CI does **not** prove Kali hardware compatibility, Tor routing,
wireless security or anonymity.

## Branches and safety

- \`legacy-v1\`: frozen legacy networking code (not production-safe).
- \`develop-v2\`: Python development and offline defensive training.
- \`main\`: preserved until the project passes go-live release gates.

Consult [Roadmap](ROADMAP.md), [Release Checklist](docs/RELEASE_CHECKLIST.md),
[Security](SECURITY.md), [Architecture](docs/ARCHITECTURE.md), and
[Provenance](CREDITS.md) before using or distributing the code.

## Contributors and licensing

Third-party legacy provenance remains under review. GhostPath v2 clean-room
Python modules are developed independently, but the repository has not yet
completed the rights review required for a public stable release.
