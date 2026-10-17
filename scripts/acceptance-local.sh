#!/usr/bin/env bash
# Read-only GhostPath v2 acceptance diagnostics for an owned Linux test VM.
# No changes to routes, DNS, firewall, MAC addresses or system services.
set -Eeuo pipefail
if [[ "$(id -u)" -eq 0 ]]; then
  echo "Run as a normal user, not root." >&2
  exit 2
fi
ROOT="$(cd -- "$(dirname -- "$0")/.." && pwd -P)"
if [[ -x "$HOME/.local/bin/ghostpath-v2" ]]; then
  APP="$HOME/.local/bin/ghostpath-v2"
elif [[ -x "$ROOT/.venv/bin/ghostpath" ]]; then
  APP="$ROOT/.venv/bin/ghostpath"
else
  echo "Install GhostPath v2 with scripts/install-user.sh or setup-dev.sh first." >&2
  exit 2
fi
if [[ "$(uname -s)" != "Linux" ]]; then
  echo "Only Linux is supported." >&2
  exit 2
fi
WORK="$(mktemp -d)"
trap 'rm -rf -- "$WORK"' EXIT

# Fingerprints only: no sensitive IP addresses or MACs in logs.
snapshot() {
  if [[ -r /etc/resolv.conf ]]; then
    sha256sum -- /etc/resolv.conf | cut -d ' ' -f 1
  else
    echo "resolver-unavailable"
  fi
  if command -v ip >/dev/null 2>&1; then
    ip -4 route show table main 2>/dev/null | sha256sum | cut -d ' ' -f 1
    ip -6 route show table main 2>/dev/null | sha256sum | cut -d ' ' -f 1
  else
    echo "route-reader-unavailable"
  fi
  if [[ -r /proc/sys/net/ipv4/ip_forward ]]; then
    sha256sum -- /proc/sys/net/ipv4/ip_forward | cut -d ' ' -f 1
  else
    echo "forward-state-unavailable"
  fi
}

snapshot > "$WORK/before"
"$APP" --version > "$WORK/version"
"$APP" doctor --json > "$WORK/doctor"
"$APP" status --json > "$WORK/status"
"$APP" privacy status --json > "$WORK/privacy"
"$APP" wifi audit --json > "$WORK/wifi"
"$APP" mac status --json > "$WORK/mac"
"$APP" defense demo --scenario normal --json > "$WORK/offline"
"$APP" release-check --json > "$WORK/gates"

"$APP" release-check --json | grep -q '"stable_release_approved": false'
snapshot > "$WORK/after"

if ! cmp -s "$WORK/before" "$WORK/after"; then
  echo "FAIL: A network-state fingerprint changed during diagnostics." >&2
  echo "This can have another cause; review your VM state before proceeding." >&2
  exit 1
fi
echo "PASS: GhostPath v2 read-only diagnostic CLI smoke test."
echo "PASS: DNS/route/forwarding fingerprints unchanged."
echo "PASS: Stable release remains blocked."
echo "LIMITATION: This does not inspect nftables as a normal user, verify Tor routing,"
echo "or replace real Kali Wi-Fi/GUI/hardware/security testing."
