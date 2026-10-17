# GhostPath v2 — User Guide

## Scope
This guide covers the Python \`develop-v2\` branch (2.0.0a2).
All privacy features are read-only diagnostics, and all DDoS learning is
offline. GhostPath does not guarantee anonymity or prevent attacks.

## 1 — Fresh installation on Kali
Use a normal unprivileged account with Python 3.11+ and a Kali test VM.

\`\`\`bash
cd ~/Desktop
git clone -b develop-v2 https://github.com/vishaalzala/GhostPath.git GhostPath-v2
cd GhostPath-v2
bash scripts/setup-dev.sh
.venv/bin/ghostpath doctor
\`\`\`

Do not run \`INSTALL.sh\` or \`ghostpath-on/off\` from the legacy project.
If you previously ran the old tool and your DNS/firewall is damaged,
restore a known-good VM snapshot or seek device administrator help before
testing new software. GhostPath v2 cannot repair unknown old configurations.

## 2 — CLI essentials
Commands are run through \`.venv/bin/ghostpath\` when not using an activated
virtual environment. Run \`--help\` for available subcommands. Add
\`--json\` at the end of supported commands for programmatic output.

- \`ghostpath doctor\`: check installed components and status.
- \`ghostpath tor status\`: check available Tor service units.
- \`ghostpath proxy status\`: check Privoxy installation/status.
- \`ghostpath privacy status\`: test a loopback-only SOCKS handshake and
  describe DNS resolver configuration.
- \`ghostpath status\`: summarize available diagnostics.

A SOCKS response means only a local proxy is responding. It does NOT
establish an exit IP, anonymity, leak prevention or active routing.

## 3 — MAC Privacy Manager
\`ghostpath mac status --json\` shows the number and interface names
without including raw addresses in the new privacy summary.
\`ghostpath mac profiles\` describes permanent, stable and random modes.
\`ghostpath mac plan random\` previews a profile; it does not apply it.
Actual changes are blocked until recovery and compatibility tests pass.

A MAC address cannot be hidden from the local network while an interface
is communicating. Randomisation can reduce persistent identification.

## 4 — Wi-Fi Security Audit
\`ghostpath wifi audit\` evaluates cached connected-network encryption
labels for the user's authorised connection. It may flag open or legacy
wireless security, but cannot verify PMF or detect every vulnerability.
The audit redacts SSIDs in its report; \`wifi status\` may show the connected
network name, so avoid publishing that raw output.

For a capture you own or are permitted to examine:
\`ghostpath wifi capture --file sample.pcap --json\`
This reads **offline** classic PCAP metadata; never downloads packets from
someone else's network or enables monitor mode. The app does not crack
passwords, impersonate APs, or disconnect devices.

## 5 — DDoS Defence & Simulation
Run \`ghostpath defense demo --scenario surge --json\` to inspect a
deterministic synthetic event surge.
Run \`ghostpath defense demo --scenario normal --json\` for a baseline.
Import an authorised local CSV file:

\`\`\`csv
minute,requests,errors
0,105,5
1,109,4
2,101,5
3,122,9
4,800,75
\`\`\`

Save as \`events.csv\`, then use
\`ghostpath defense analyze --file events.csv --json\`.

The detector compares data to an early fixed baseline using a simple
threshold. An alert is an **anomaly**, not proof of an attack. Verify
service health, source logs, legitimate campaigns and false positives.
\`ghostpath defense counters\` reports cumulative local interface counters;
these are not packet rates.

\`ghostpath defense capture --file example.pcap\` reads metadata only.
It never generates a flood or operates against public targets.

## 6 — Learning centre
\`ghostpath labs list\` displays available offline lessons.
\`ghostpath labs run traffic-anomaly\` demonstrates volume alerts.
Other lessons: \`traffic-baseline\`, \`wifi-hardening\`, \`mac-privacy\`.

## 7 — Desktop GUI
If you have a desktop environment and can install Qt:

\`\`\`bash
source .venv/bin/activate
python -m pip install -e '.[gui]'
ghostpath gui
\`\`\`

The GUI shows Dashboard, Privacy, MAC Privacy, Wi-Fi Audit,
DDoS Defence and Learning Labs. It does not need root permissions.
If the interface fails to open, use the CLI and check PySide6 availability.

## 8 — Local reports
\`ghostpath report create --output my-report.json\` creates a **new**
private report. Existing paths cannot be overwritten. Review the report
before sharing; reports intentionally omit MACs/SSIDs and packet contents.

## 9 — Updating
In the v2 checkout:
\`\`\`bash
git pull origin develop-v2
source .venv/bin/activate
python -m pip install --no-deps -e .
bash scripts/test.sh
\`\`\`

## 10 — Troubleshooting
- Not found: ensure your venv is active or invoke \`.venv/bin/ghostpath\`.
- Missing Tor or Privoxy: status reports absence; v2 does not auto-install.
- systemd unavailable: status can show unknown and no network change occurs.
- No Wi-Fi detected: NetworkManager or physical wireless support may be absent.
- GUI missing: install optional GUI extras in the virtual environment.
- PCAPNG rejected: convert authorised captures to classic PCAP externally.
- Reports fail: choose a writable new filename ending in \`.json\`.

## 11 — No-go boundaries
Do not use this alpha for sensitive anonymity needs, real-world DDoS
generation, unauthorised wireless access, or production firewall changes.
See the release checklist for unfinished testing.
