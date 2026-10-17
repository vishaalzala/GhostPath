# GhostPath v2 Architecture

The CLI and future GUI share an unprivileged Python diagnostics core.
This alpha is read-only: it reads sysfs and runs narrowly allowlisted
diagnostics with shell=False and bounded timeouts.

| Area | Module |
| --- | --- |
| CLI and JSON | src/ghostpath/cli.py |
| Aggregate diagnostics | src/ghostpath/diagnostics.py |
| Tor and Privoxy service inspection | src/ghostpath/services.py |
| Local interfaces and cached connected Wi-Fi | src/ghostpath/network.py |
| Approved subprocess calls | src/ghostpath/core/runner.py |

A running Tor service does not prove application traffic uses Tor;
routing_verified remains false until an independently verified path exists.

The initial command runner cannot change routing, DNS, firewall, MAC, radio,
or process service state. Do not operate the whole application as root.

Any future privileged helper must have explicit authorization, capability
limits, transaction snapshots, rollback, restart recovery, and fault tests.

Initial compatibility target: Python 3.11+, Kali Linux test VMs;
other distributions require documented tests before declaring support.
