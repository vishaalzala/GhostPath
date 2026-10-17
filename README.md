# GhostPath

**Linux Privacy & Network Security Toolkit**

GhostPath is an educational Linux privacy and network-security project for learning Tor routing, network diagnostics and safe configuration management on owned or authorized systems.

> **Status:** Rebranded legacy scripts. The original networking logic has not been modernized, verified or made production-ready. Do not run the installer on a daily-use machine; use an isolated VM and snapshot.

## Available source components

- `ghostpath` main command-line program
- `ghostpath-on` and `ghostpath-off` helper scripts
- `ghostpath-gui` legacy GTKdialog interface
- Tor, Privoxy and Polipo legacy configurations
- Network configuration, firewall and DNS management scripts

These filenames correspond to the newly prepared source ZIP. **The ZIP and its source files are not yet present in this GitHub repository.** Download the prepared archive from the project delivery and review locally before use.

## Getting started

1. Use a disposable Kali or Debian VM for evaluation.
2. Inspect `INSTALL.sh` and all scripts before running them.
3. Create a snapshot before testing any scripts that change firewall or DNS settings.
4. Treat installation, automatic restoration and distribution compatibility as unverified.

There is no supported production installation procedure yet.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned secure rollback, nftables, modern Tor integration, leak checks, GUI, packaging and automated tests.

## Responsible use

For ethical research and systems or networks you own or are authorized to administer. Tor does not guarantee anonymity.

## Attribution and licensing

Original script contributors are acknowledged in source comments. The supplied archive did not contain a clearly identified license; confirm permissions before publishing derivative code publicly.
