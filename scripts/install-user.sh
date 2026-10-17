#!/usr/bin/env bash
# User-scoped installation only; never changes the system network.
set -Eeuo pipefail
umask 077
if [[ "$(id -u)" -eq 0 ]]; then echo "Run as a normal user, not root." >&2; exit 1; fi
if [[ $# -gt 1 ]]; then echo "Usage: bash scripts/install-user.sh [--gui]" >&2; exit 2; fi
GUI="no"
if [[ $# -eq 1 ]]; then
  if [[ "$1" != "--gui" ]]; then echo "Expected --gui" >&2; exit 2; fi
  GUI="yes"
fi
ROOT="$(cd -- "$(dirname -- "$0")/.." && pwd -P)"
DATA="$HOME/.local/share"
PREFIX="$DATA/ghostpath-v2"
BIN="$HOME/.local/bin/ghostpath-v2"
if [[ -e "$PREFIX" || -L "$PREFIX" || -e "$BIN" || -L "$BIN" ]]; then
  echo "A GhostPath v2 user installation exists. Run update-user.sh." >&2
  exit 1
fi
command -v python3 >/dev/null || { echo "Python 3 is not installed." >&2; exit 1; }
mkdir -p -- "$DATA" "$HOME/.local/bin"
STAGE="$(mktemp -d "$DATA/.ghostpath-v2-stage.XXXXXXXX")"
cleanup() { if [[ -n "$STAGE" && -d "$STAGE" ]]; then rm -rf -- "$STAGE"; fi; }
trap cleanup EXIT
python3 -m venv "$STAGE/venv"
if [[ "$GUI" == "yes" ]]; then
  "$STAGE/venv/bin/python" -m pip install "$ROOT[gui]"
else
  "$STAGE/venv/bin/python" -m pip install --no-deps "$ROOT"
fi
"$STAGE/venv/bin/python" -m ghostpath --version
cat > "$STAGE/launch.sh" <<'LAUNCHER'
#!/usr/bin/env bash
set -Eeuo pipefail
exec "$HOME/.local/share/ghostpath-v2/venv/bin/python" -m ghostpath "$@"
LAUNCHER
chmod 700 "$STAGE/launch.sh"
if [[ -e "$PREFIX" || -L "$PREFIX" || -e "$BIN" || -L "$BIN" ]]; then
  echo "Installation collision: nothing replaced." >&2
  exit 1
fi
mv -- "$STAGE" "$PREFIX"
STAGE=""
if ! ln -s -- "$PREFIX/launch.sh" "$BIN"; then
  echo "Launcher creation failed. Installation remains at $PREFIX." >&2
  exit 1
fi
"$BIN" --version
echo "Installed user-scoped GhostPath v2. Run: $BIN doctor"
echo "No DNS, firewall, MAC, Tor or Wi-Fi system configuration modified."
