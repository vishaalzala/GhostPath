# GhostPath v2 Roadmap

This document is a **plan**, not a list of completed features.

## Phase 1 — Safety foundation (highest priority)
- [ ] Review legacy installer, network mutations, dependencies and permissions.
- [ ] Implement backup, state capture, rollback, and safe uninstall.
- [ ] Add idempotent operations and validate configuration before activation.
- [ ] Remove obsolete dependencies and unsafe privacy claims.

## Phase 2 — Network engine
- [ ] Add maintained Tor service integration and readiness checks.
- [ ] Implement nftables compatibility checks and safe firewall transaction handling.
- [ ] Integrate safely with NetworkManager and systemd-resolved.
- [ ] Provide DNS/IPv4/IPv6 leak tests and independent connectivity verification.
- [ ] Test fail-closed behaviour, emergency stop, and recovery after reboot.

## Phase 3 — User experience
- [ ] Build an accessible Python CLI.
- [ ] Add a non-root GUI with a limited privileged helper.
- [ ] Provide clear network state, logs and actionable errors.

## Phase 4 — Educational privacy tools
- [ ] Optional I2P support.
- [ ] Network diagnostics restricted to owned or authorized environments.
- [ ] Optional MAC randomization with dependable restore.
- [ ] Safe learning guides and redactable diagnostic exports.

## Phase 5 — Quality and release
- [ ] Add unit and integration tests.
- [ ] Test in disposable supported Kali/Debian/Parrot VMs.
- [ ] Add CI static analysis, dependency checks and software bill of materials.
- [ ] Release versioned packages with documented installation and uninstall.
- [ ] Publish tested compatibility matrix and release notes.

## Release gate
Do not call GhostPath v2 stable until configuration restoration, DNS protection, firewall rollback, reboot handling, and uninstall have passed regression testing.
