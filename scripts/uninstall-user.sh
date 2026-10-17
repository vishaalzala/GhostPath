#!/usr/bin/env bash
# Removes only verifiably managed user-scoped files, never system settings.
set -Eeuo pipefail
if [[ "$(id -u)" -eq 0 ]]; then echo "Do not uninstall as root." >&2; exit 1; fi
if [[ $# -ne 0 ]]; then echo "Usage: bash scripts/uninstall-user.sh" >&2; exit 2; fi
PREFIX="$HOME/.local/share/ghostpath-v2"
BIN="$HOME/.local/bin/ghostpath-v2"
if [[ -L "$PREFIX" ]]; then
  echo "Refusing to remove a symlinked installation directory." >&2; exit 1
fi
if [[ ! -L "$BIN" || "$(readlink -- "$BIN")" != "$PREFIX/launch.sh" ]]; then
  echo "Launcher is not GhostPath-managed; refusing removal." >&2; exit 1
fi
if [[ ! -x "$PREFIX/venv/bin/ghostpath" ]]; then
  echo "Installed program is missing; refusing automatic removal." >&2; exit 1
fi
rm -- "$BIN"
rm -rf -- "$PREFIX"
echo "GhostPath v2 user installation removed. Network state unchanged."
