# GhostPath

**Linux Privacy & Network Security Toolkit**

> **Status:** Legacy Anonym8 codebase undergoing a proposed modernization. Not production-ready or verified on current Kali Linux releases.

GhostPath is an educational project exploring Linux networking, privacy routing, Tor, proxy configuration, and defensive network diagnostics.

## What's in this repository?

The original Anonym8 project contains legacy shell scripts for Tor-based networking, proxy configuration, DNS management, firewall rules, hostname/MAC changes, and a desktop launcher. These components have **not** yet been modernized or security-tested. The project name and documentation have been refreshed, but a stable GhostPath v2 application has **not** been released.

## Important safety warning

The legacy installer and scripts can change system DNS settings, proxy configuration, and firewall rules. Do **not** run the legacy installer on a daily-use machine. Use a disposable, isolated Linux VM, snapshot it first, and inspect scripts before execution. Tor is not a guarantee of anonymity.

## Current features (legacy)

- Tor integration and transparent proxy configuration
- Privoxy and Polipo configuration files
- DNS and iptables-based network configuration
- MAC address and hostname management
- CLI entry points `anonym8`, `anON` and `anOFF`
- Legacy Linux desktop launcher and GUI

**Availability is not compatibility:** listed features are present in the old source, but functionality on recent distributions remains unverified.

## GhostPath v2 goals (planned, not implemented)

- Modern nftables-compatible firewall handling
- Network configuration backup and reliable rollback
- Tor bootstrap health checks and SOCKS integration
- DNS and IPv6 leak diagnostics
- Optional fail-closed kill switch with recovery path
- Privilege separation and secure configuration validation
- Modern GUI and documented CLI
- Automated tests, reproducible packages, and CI security checks
- Guided educational labs for owned or authorized systems

See [ROADMAP.md](ROADMAP.md) for the implementation priorities.

## Getting started (safe inspection)

1. Use a throwaway Kali/Debian VM for research.
2. Review the source and configuration files before running anything.
3. Read [README_LEGACY.md](README_LEGACY.md) for historical documentation; its installation steps are not endorsed.
4. Track modernization work in the roadmap.
5. Do not enable firewall or DNS-changing scripts without a validated rollback and VM snapshot.

There is **no supported v2 installation command** yet.

## Responsible use

Use GhostPath only on devices, networks, and test environments you own or are explicitly authorized to manage. Do not present this toolkit as a foolproof anonymity solution.

## Contributions

Issues and pull requests covering reliability, packaging, documentation, privacy diagnostics, test coverage, and secure recovery behaviour are welcome. Please avoid exposing private IP addresses, credentials, or personal data in diagnostics.

## Project heritage

GhostPath is based on the educational Anonym8 project. Its original documentation is preserved in [README_LEGACY.md](README_LEGACY.md). Existing command/file names remain legacy identifiers until a tested migration is implemented.
