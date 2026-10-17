# GhostPath v2 — User-scoped installation and maintenance

GhostPath v2 is currently a development alpha. It runs passive Linux
diagnostics and offline defensive exercises. It **does not** provide
verified anonymity or system-wide routing, and it is not a replacement for
the existing networking configuration.

## Requirements
- A Linux account without root privileges (Kali or Debian for testing).
- Python 3.11+ with venv support and pip installed by your distribution.
- A normal internet connection for Python package dependencies.
- Do not run legacy GhostPath v1 scripts or the v1 installer on your main OS.

## Clone the development code
    git clone --branch develop-v2 https://github.com/vishaalzala/GhostPath.git GhostPath-v2
    cd GhostPath-v2

## Install only for your user
    bash scripts/install-user.sh
    ~/.local/bin/ghostpath-v2 --version
    ~/.local/bin/ghostpath-v2 doctor --json

The installer places the isolated Python environment under
~/.local/share/ghostpath-v2 and creates the launcher
~/.local/bin/ghostpath-v2. It refuses root and existing installations,
and does not install operating-system packages or change network state.

For a Qt desktop environment, you can try:
    bash scripts/install-user.sh --gui
    ~/.local/bin/ghostpath-v2 gui

The GUI still requires manual real-desktop testing.

## Upgrade
Close any running GhostPath GUI, pull the development branch, then run:

    git pull --ff-only origin develop-v2
    bash scripts/update-user.sh
    ~/.local/bin/ghostpath-v2 doctor

If your original installation included the optional GUI, include --gui
in the update command. The updater stages a new environment and preserves
the previous environment until the new launcher has been verified.

## Remove the development installation
    bash scripts/uninstall-user.sh

The uninstaller checks that the launcher points to a managed GhostPath
environment. It refuses to remove unknown/symlinked directory targets
and never changes network or firewall configuration.

## Is this the same as the old GhostPath?
No. This v2 installation uses the distinct command ghostpath-v2.
Old v1 commands and system files are not automatically removed or migrated.
Do not mix versions. If you previously ran the legacy script and it
altered DNS or firewall state, restore using a verified OS backup/VM snapshot
before installing v2. V2 cannot repair arbitrary historical configurations.

## Troubleshooting
- Permission denied: use a normal user, not the Kali root shell.
- Missing venv: install Python's distribution-packaged venv support.
- GhostPath not found: use ~/.local/bin/ghostpath-v2 or add ~/.local/bin
  to your shell PATH.
- The user installer reports an existing installation: use update-user.sh.
- Broken or unexpected launcher: do not force-delete directories; manually
  inspect its target before cleanup.
- No desktop display: use the CLI, which does not need Qt.
- Installed Tor is not evidence that GhostPath is routing anything through it.
