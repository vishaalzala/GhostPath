"""Evidence-based release gates: default denies stable release."""
from __future__ import annotations

REQUIRED = [
    "Kali and Debian disposable VM smoke tests",
    "System/network change restoration after crash or reboot",
    "Independent security and privacy review",
    "Dependency/license/provenance audit",
    "Packaging, upgrade and uninstall verification",
    "Accessible GUI and integrated scenario testing",
    "Release artifact signatures and provenance",
]


def readiness() -> dict[str, object]:
    return {
        "stable_release_approved": False,
        "reason": "Automated unit tests do not replace platform and recovery verification.",
        "requires_manual_evidence": REQUIRED,
        "network_mutation_enabled": False,
        "supported_mode": "local diagnostics and offline educational analysis",
    }
