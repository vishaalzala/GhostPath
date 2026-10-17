# GhostPath v2 — Build provenance and software inventory

GhostPath v2 development artifacts are not stable production releases.
The development build workflow creates a wheel, source archive, CycloneDX
software bill of materials, SHA-256 checksums and GitHub build attestation.

## Viewing artifacts

1. In GitHub Actions select "GhostPath Development Artifact Verification".
2. Open a successful develop-v2 run.
3. Download ghostpath-v2-verified-development.
4. Read SHA256SUMS and ghostpath-runtime.cdx.json.
5. Verify the attestation with a recent GitHub CLI:

    gh attestation verify ghostpath-*.whl --repo vishaalzala/GhostPath

An attestation associates a build artifact with GitHub workflow provenance.
It does NOT prove anonymity, safety or absence of vulnerabilities.

## Scope

The runtime SBOM is limited to packages installed from the core GhostPath
wheel in an isolated Python environment. It does not include OS Tor,
Privoxy, NetworkManager, or optional Qt GUI dependencies.

## Licensing

The historical legacy shell code has uncertain redistribution rights.
Stable redistribution of that historical source and any inherited assets
is blocked until rights are clarified. The development artifacts are
for evaluation and authorised testing, pending review.

## Release gate

Signature/provenance evidence is only one gate; owner approval, real
Kali VM testing, GUI QA and independent security review are also required.
