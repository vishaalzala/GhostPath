# Contributing to GhostPath

1. Work on feature branches off develop-v2.
2. Keep changes local-first, defensive and reviewable.
3. Do not introduce active wireless attacks, uncontrolled flood generation,
   stealthy tracking or credential interception.
4. Add tests for failures, missing dependencies, privacy and resource caps.
5. Run bash scripts/test.sh as a normal unprivileged user.
6. Include threat model changes in docs/ARCHITECTURE.md.
7. Do not alter live firewall, DNS or network identities without approved
   architectural design, restoration testing and explicit user consent.
8. Avoid logging credentials, IP addresses, MACs or SSIDs by default.
9. Review upstream licenses; do not copy third-party sources without rights.
10. Use draft PRs until CI and reviewers accept the changes.

Before submitting a new feature, document its scope, data sources, failures,
supported Linux environments, test evidence, resource limits and rollback.
