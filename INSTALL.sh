#!/usr/bin/env bash
# GhostPath experimental installer: use only in a disposable Linux VM.
set -Eeuo pipefail
if (( EUID != 0 )); then echo "Run with sudo: sudo ./INSTALL.sh" >&2; exit 1; fi
cd "$(dirname "$(realpath "$0")")"
echo "Installing GhostPath legacy scripts for VM evaluation."
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y tor privoxy nyx macchanger dnsmasq libnotify-bin curl
# Do not replace live DNS, Tor, Privoxy or firewall configuration.
install -Dm755 usr/ghostpath /usr/local/bin/ghostpath
install -Dm755 usr/ghostpath-on /usr/local/bin/ghostpath-on
install -Dm755 usr/ghostpath-off /usr/local/bin/ghostpath-off
install -Dm755 etc/ghostpath.sh /usr/local/lib/ghostpath/ghostpath.sh
install -Dm644 privoxy/config /usr/local/share/ghostpath/examples/privoxy-config.legacy
install -Dm644 tor/torrc /usr/local/share/ghostpath/examples/torrc.legacy
install -Dm755 opt/ghostpath/ghostpath-gui /opt/ghostpath/ghostpath-gui
install -Dm644 ghostpath.desktop /usr/share/applications/ghostpath.desktop
if [[ -f ghostpath.png ]]; then install -Dm644 ghostpath.png /opt/ghostpath/ghostpath.png; fi
printf '\nGhostPath installed with Tor, Privoxy and Nyx dependencies.\n'
printf 'WARNING: Network routing/firewall behavior is still unverified. Only use a disposable VM.\n'
printf 'Commands: ghostpath, ghostpath-on, ghostpath-off; Nyx: ghostpath start_nyx\n'
