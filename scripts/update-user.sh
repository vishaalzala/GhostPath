#!/usr/bin/env bash
# Atomic-ish local-user venv replacement with verified launcher and rollback.
set -Eeuo pipefail
umask 077
if [[ "$(id -u)" -eq 0 ]]; then echo "Do not update as root." >&2; exit 1; fi
if [[ $# -gt 1 ]]; then echo "Usage: bash scripts/update-user.sh [--gui]" >&2; exit 2; fi
GUI="no"
if [[ $# -eq 1 ]]; then
  if [[ "$1" != "--gui" ]]; then echo "Expected --gui" >&2; exit 2; fi
  GUI="yes"
fi
ROOT="$(cd -- "$(dirname -- "$0")/.." && pwd -P)"
DATA="$HOME/.local/share"
PREFIX="$DATA/ghostpath-v2"
BIN="$HOME/.local/bin/ghostpath-v2"
if [[ ! -d "$PREFIX" || -L "$PREFIX" || ! -L "$BIN" ||
  "$(readlink -- "$BIN")" != "$PREFIX/launch.sh" ]]; then
  echo "User installation missing or launcher is not GhostPath-managed." >&2
  exit 1
fi
STAGE="$(mktemp -d "$DATA/.ghostpath-v2-update.XXXXXXXX")"
BACKUP=""
cleanup() {
  if [[ -n "$STAGE" && -d "$STAGE" ]]; then rm -rf -- "$STAGE"; fi
  if [[ -n "$BACKUP" && -d "$BACKUP" ]]; then
    if [[ ! -e "$PREFIX" ]]; then mv -- "$BACKUP" "$PREFIX"; else
      echo "Previous installation kept at $BACKUP" >&2
    fi
  fi
}
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
BACKUP="$(mktemp -d "$DATA/.ghostpath-v2-backup.XXXXXXXX")"
rmdir -- "$BACKUP"
mv -- "$PREFIX" "$BACKUP"
if ! mv -- "$STAGE" "$PREFIX"; then
  mv -- "$BACKUP" "$PREFIX"
  BACKUP=""
  exit 1
fi
STAGE=""
if ! "$BIN" --version; then
  echo "Upgrade validation failed; restoring previous installation." >&2
  mv -- "$PREFIX" "$BACKUP.bad"
  mv -- "$BACKUP" "$PREFIX"
  BACKUP=""
  exit 1
fi
rm -rf -- "$BACKUP"
BACKUP=""
echo "GhostPath v2 update succeeded. Close any previous GUI before updating."
