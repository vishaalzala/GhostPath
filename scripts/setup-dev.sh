#!/usr/bin/env bash
# GhostPath v2 developer setup: no sudo and no system configuration changes.
set -Eeuo pipefail
if [[ "$(id -u)" -eq 0 ]]; then
  echo "Run this as an ordinary user, not root." >&2
  exit 1
fi
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required." >&2
  exit 1
fi
python3 -m venv .venv
"$ROOT/.venv/bin/python" -m pip install --no-deps -e "$ROOT"
echo "GhostPath v2 alpha installed locally in .venv."
echo "Try: $ROOT/.venv/bin/ghostpath doctor --json"
echo "No firewall, DNS, routing, MAC or Wi-Fi settings were changed."
