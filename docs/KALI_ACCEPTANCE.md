# GhostPath v2 — Real Kali Acceptance Test

This is a manual release gate. Passing container CI is NOT evidence of
working physical Wi-Fi hardware or a real graphical Kali desktop.

## Before testing
- Use a disposable, updated Kali virtual machine with a snapshot.
- Sign in as a regular non-root user.
- Do not run the old GhostPath v1 installer or start/stop scripts.
- Do not publish MACs, IPs, SSIDs or usernames in evidence.

## Checklist
1. Clone develop-v2 into a new directory and run:
       bash scripts/install-user.sh
2. Run:
       ~/.local/bin/ghostpath-v2 doctor --json
       ~/.local/bin/ghostpath-v2 release-check --json
   Stable release approval must remain false.
3. Run scripts/acceptance-local.sh as an ordinary user.
4. Test the connected-network Wi-Fi audit with an owned adapter and
   verify that it does not initiate new scans or disclose identifiers.
5. Import only supplied synthetic training files and authorised PCAPs.
6. Test the optional GUI in real X11 or Wayland: tabs, focus, scrolling,
   keyboard access, error states and DPI scaling.
7. Run the user-scope updater, including a simulated failure, and check
   that a prior installation remains available.
8. Run the user-scope uninstaller and verify it removes only managed files.
9. Reboot and confirm network, DNS, routes and firewall settings unchanged.
10. Record OS/driver/Qt/package versions, test date, outcomes and redacted
    screenshots for independent review.

## Release conditions

Manual evidence, owner approval, third-party license/provenance checks,
and independent security review are required for stable distribution.
Read-only beta checks do not justify enabling system-wide firewall/DNS
changes, live MAC mutations or any disruptive wireless/network behaviour.
