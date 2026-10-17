# GhostPath v2 — Practical User Guide

**Development build: v2.0.0a2. Only local diagnostics and offline defensive
training are available. It is NOT an anonymising VPN or Tor router.**

## 1. Installation on Kali Linux

Use a normal Kali user account (not the root@kali prompt):

    git clone -b develop-v2 https://github.com/vishaalzala/GhostPath.git GhostPath-v2
    cd GhostPath-v2
    bash scripts/setup-dev.sh
    .venv/bin/ghostpath --version

This creates a private Python virtual environment. It does not
change any system firewall, DNS, Wi-Fi or MAC settings.

## 2. System health

    .venv/bin/ghostpath doctor --json
    .venv/bin/ghostpath status --json

These show available local services. Tor running does not prove
that traffic uses Tor. The application does not enable privacy routing.

## 3. Privacy status

    .venv/bin/ghostpath privacy status --json
    .venv/bin/ghostpath tor status --json
    .venv/bin/ghostpath proxy status --json

This checks local Tor SOCKS reachability and resolver configuration.
It is not an external DNS-leak test or proof of anonymous browsing.

## 4. MAC privacy

    .venv/bin/ghostpath mac status --json
    .venv/bin/ghostpath mac profiles --json
    .venv/bin/ghostpath mac plan stable --json

The plan shows what a privacy profile would mean, but **does not
apply a new MAC**. MAC addresses remain visible on their local link.

## 5. Wi-Fi review

    .venv/bin/ghostpath wifi status --json
    .venv/bin/ghostpath wifi audit --json

The current connection is inspected without starting a scan.
For a router you own, write a local settings JSON file (example
available in examples/router.json):

    {
      "security": "WPA3",
      "wps_enabled": false,
      "pmf": "required",
      "guest_isolation": true
    }

Run:

    .venv/bin/ghostpath wifi config --file examples/router.json --json

No Wi-Fi password attempt, connection or radio transmission occurs.
To analyse *existing authorised* classic PCAP files (not PCAPNG):

    .venv/bin/ghostpath wifi capture --file ./owned-capture.pcap --json

Only bounded frame-type metadata is output.

## 6. DDoS Defence & Incident Analysis

To explore synthetic traffic counts with a baseline:

    .venv/bin/ghostpath defense demo --scenario surge --json

To analyse your saved/offline event counts:

    .venv/bin/ghostpath defense analyze --file examples/traffic.csv --json

CSV columns: minute,requests,errors. Values must be nonnegative
integers; minutes must increase. A flagged rise is not proof of attack.

To aggregate offline Suricata alert events:

    .venv/bin/ghostpath defense eve --file examples/eve.jsonl --json

Source/destination IPs are omitted in the aggregate report.

## 7. Learning and safe labs

    .venv/bin/ghostpath labs list --json
    .venv/bin/ghostpath labs run traffic-anomaly --json
    .venv/bin/ghostpath learn list --json
    .venv/bin/ghostpath learn show wifi --json

These lessons and simulations work offline and do not send any
disruptive traffic.

## 8. Reports

    .venv/bin/ghostpath report create --output findings.json
    .venv/bin/ghostpath report html --output findings.html

Reports are written locally as new private files and refuse to
overwrite an existing file. The HTML report is escaped; you can open
it in a browser and print to PDF. Review content before sharing.

## 9. GUI

    source .venv/bin/activate
    python -m pip install '.[gui]'
    ghostpath gui

The optional desktop view shows status, MAC plans, Wi-Fi posture,
defensive labs, offline file imports, education and reports.
Do not run the desktop interface as root.

## 10. Updating and troubleshooting

Update the v2 checkout:

    git pull origin develop-v2
    bash scripts/setup-dev.sh
    bash scripts/test.sh

Common issues:
- Module/command not found: run the executable inside .venv/bin.
- Missing python3-venv: install it from Kali APT.
- Missing Tor or NetworkManager: those diagnostics report unavailable.
- GUI fails: ensure a graphical Linux session and PySide6 in the venv.
- Existing legacy GhostPath broke internet: use your VM snapshot;
  the Python v2 utility does not undo old legacy system changes.
- File analysis error: check offline format and bounded file sizes.
- Report already exists: select a different output filename.

## What is still excluded?

This build cannot anonymise entire systems, change MAC addresses,
test Wi-Fi passwords, flood networks, enforce a kill switch,
or automatically repair external network configuration.
See the release checklist for the remaining tests and engineering.
