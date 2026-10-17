# Anonym8 — legacy documentation reference

Original project: **Anonym8 (Privacy Friend)** by **@HiroshimanRise**.

The original documentation describes transparent proxy routing through Tor, I2P, Privoxy and Polipo, DNS modification, MAC address changes, hostname changes, and RAM/cache/swap cleaning. It claimed testing on Debian, Kali and Parrot.

## Historical dependencies
Tor, macchanger, resolvconf, dnsmasq, polipo, privoxy, arm, libnotify, curl, bleachbit; the GUI additionally expected GTKdialog, libvte.so.9 and I2P.

## Legacy installer
The older Anonym8 project shipped an `INSTALL.sh` script intended to be run as root. **Do not run that historical installer on a daily-use system.** It mutates firewall, DNS and system network configuration, and compatibility with current distributions has not been verified.

## Historical browser advice
The original documentation recommended Firefox and extensions, some of which are now outdated. Do not assume those recommendations are current.

This document is a condensed historical reference. The full original README is retained in the downloadable source archive from the project migration, but has not yet been uploaded here verbatim. See [README.md](README.md) for current project status and [ROADMAP.md](ROADMAP.md) for proposed changes.
