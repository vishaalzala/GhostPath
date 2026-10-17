# GhostPath

**Linux Privacy & Network Security Toolkit**

GhostPath is a Linux-based, education-focused project for studying Tor routing, proxy settings, network diagnostics, and privacy controls on devices and lab networks you own or have permission to manage.

> **Development status:** This is a rebranded, untested legacy codebase. Changing names does not modernize its networking behaviour. **Do not run the installer on your everyday operating system.** Use a disposable VM and a snapshot. No anonymity guarantee is provided.

## What is included today

- `ghostpath` — main command-line entry point
- `ghostpath-on` / `ghostpath-off` — historical convenience scripts
- `ghostpath-gui` — older GTKdialog launcher
- Tor, Privoxy, and Polipo example configurations
- Scripts interacting with firewall rules, DNS settings, network identity, and services

**Not yet implemented or validated:** current Kali compatibility, nftables migration, modern GUI, reliable rollback, kill switch, CI tests, or production release.

## Repository layout

```text
GhostPath/
├── README.md
├── ROADMAP.md
├── INSTALL.sh
├── ghostpath.desktop
├── ghostpath.png
├── etc/ghostpath.sh
├── usr/ghostpath
├── usr/ghostpath-on
├── usr/ghostpath-off
├── opt/ghostpath/ghostpath-gui
├── tor/torrc
├── polipo/config
└── privoxy/config
```

## Getting started safely

1. Clone the repository into a dedicated, isolated Linux VM.
2. Read `INSTALL.sh` and all scripts before running them.
3. Make a VM snapshot, especially before any change to DNS or firewall rules.
4. Consider the bundled installation process *historical and unsupported* until its rollback and distro checks have been tested.

There is no recommended production installation command at this stage.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the modernization checklist.

## Responsible use

Run network experiments only on systems and networks you control or for which you have explicit authorization. Tor is not a promise of complete anonymity. Never rely on this unreleased tool to protect sensitive activity.

## Credits and licensing

Original script comments attribute work to **HiroshimanRise**, **ParrotSec**, **cysec666**, and other contributors. Contributor attribution is retained in source files. The source archive did not include a clearly identified license; redistribution rights should be confirmed before a public release.


## Kali dependency update (October 2026)

- **Nyx** replaces the outdated Tor ARM monitoring package (`ghostpath start_nyx`).
- **Privoxy** provides the HTTP proxy service (`ghostpath start_http_proxy`, `stop_http_proxy`, `status_http_proxy`).
- The installer checks APT failures and places example configuration files under `/usr/local/share/ghostpath/examples/`, rather than overwriting system Tor/Privoxy configuration.
- The old firewall/DNS routing engine remains unverified. Installing dependencies is **not** proof that transparent routing works or restores networking correctly.

On a disposable VM only, inspect the installer then use `sudo ./INSTALL.sh`. Do not use this build for sensitive browsing.
