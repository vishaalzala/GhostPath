# GhostPath v2 Alpha — User Guide

GhostPath v2 is a development diagnostic utility, NOT an anonymising
traffic-routing application. Use on an owned computer with a normal
unprivileged user account.

## Install
Follow the Python venv steps in README.md on the develop-v2 branch.

## Confirm version
Run: `ghostpath --version`. Expect v2.0.0a1.

## Basic health
Run: `ghostpath doctor --json`. Check dependencies, systemd services,
NetworkManager and any root-user warning. No network settings are changed.

## Tor and Privoxy
Run `ghostpath tor status` and `ghostpath proxy status`.
A service may be missing or inactive; neither result means traffic is
anonymously routed. GhostPath alpha will not start these services.

## MAC status
Run `ghostpath mac status --json`.
This shows locally visible MACs but does NOT change them. Do not post
identifying addresses publicly.

## Wi-Fi status
Run `ghostpath wifi status --json`. Only existing cached information
about a connected access point is displayed; no new Wi-Fi scan starts.
Wi-Fi audits and offline capture lessons are planned, not implemented.

## DDoS defence
The DDoS module is planned and will use synthetic/authorized offline data.
No active public-target disruption or traffic flooding will be provided.

## Troubleshooting
- GhostPath command missing: activate the venv, reinstall editable package.
- Tor not installed: the diagnostic still reports missing dependency.
- Unknown service status: systemd or the specific unit may be unavailable.
- Wi-Fi unavailable: check whether NetworkManager/nmcli is installed.
- If on old GhostPath: switch to develop-v2 and use its Python command.

## Updating
In the same development checkout:
`git pull origin develop-v2`; activate venv, then
`python -m pip install --no-deps -e .`.

## Reporting issues
Redact IP addresses, SSIDs, MAC addresses and other private identifiers
before attaching diagnostic output to GitHub.
