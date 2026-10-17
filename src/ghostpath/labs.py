"""Offline exercises with no external targets or network traffic."""
from __future__ import annotations

from .defense import analyze, example_events
from .wifi_audit import assess_security

LABS = {
    "traffic-baseline": "Learn how a normal traffic baseline differs from suspicious volume.",
    "traffic-anomaly": "Investigate a synthetic volume anomaly and potential false positives.",
    "wifi-hardening": "Review fictional router security modes and suggested improvements.",
    "mac-privacy": "Understand the difference between permanent, stable and random addressing.",
}


def list_labs() -> dict[str, object]:
    return {"labs": [{"id": k, "description": v} for k, v in LABS.items()],
            "offline_only": True}


def run_lab(name: str) -> dict[str, object]:
    if name not in LABS:
        raise ValueError("Unknown learning lab")
    if name == "traffic-baseline":
        result = analyze(example_events("normal"))
    elif name == "traffic-anomaly":
        result = analyze(example_events("surge"))
    elif name == "wifi-hardening":
        result = {item: assess_security(item) for item in ("OPEN", "WEP", "WPA2", "WPA3")}
    else:
        result = {
            "permanent": "Hardware address: may act as a stable local identifier.",
            "stable": "A per-network pseudonymous identifier may reduce cross-network correlation.",
            "random": "A random address may reduce persistence but does not guarantee anonymity.",
        }
    return {
        "lab": name, "description": LABS[name], "offline_only": True,
        "result": result, "complete": True,
        "next_step": "Document what the results do and do not prove.",
    }
