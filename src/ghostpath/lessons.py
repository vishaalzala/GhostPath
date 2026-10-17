"""Offline beginner-friendly cybersecurity education without attack tooling."""
from __future__ import annotations

CONTENTS = {
    "tor": (
        "Tor health versus routing",
        "A running Tor daemon alone does not mean a browser routes through Tor. "
        "A local SOCKS listener, route selection and leak resistance are separate checks.",
        "Is an active service proof of anonymity? No.",
    ),
    "mac": (
        "MAC privacy basics",
        "A MAC address is a link-local identifier. Randomisation may reduce local tracking "
        "but cannot hide an internet IP address or guarantee network anonymity.",
        "Does randomisation hide your IP? No.",
    ),
    "wifi": (
        "Defensive Wi-Fi hardening",
        "Use WPA3 where supported, review WPS, protected management frames, guest isolation "
        "and firmware updates on access points you own or administer.",
        "Can offline configuration review prove a network unhackable? No.",
    ),
    "ddos": (
        "DDoS incident recognition",
        "Use offline traffic baselines, response errors and service capacity to assess "
        "anomalies. Traffic spikes may have innocent causes and require investigation.",
        "Is a traffic spike proof of DDoS? No.",
    ),
    "report": (
        "Defensive incident reporting",
        "Explain scope, evidence, limitations and remediation. Remove credentials, "
        "hostnames, private addresses and personal details before sharing reports.",
        "Should raw private IPs be placed in public issues? No.",
    ),
}


def list_lessons() -> dict[str, object]:
    return {"lessons": [{"slug": k, "title": v[0]} for k, v in CONTENTS.items()], "offline_only": True}


def read_lesson(slug: str) -> dict[str, object]:
    if slug not in CONTENTS:
        raise ValueError("Unknown lesson")
    title, lesson, question = CONTENTS[slug]
    return {"slug": slug, "title": title, "lesson": lesson, "check_yourself": question, "offline_only": True}
