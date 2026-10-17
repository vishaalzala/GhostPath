"""Human-readable presentation models for defensive GhostPath data.

Pure Python: no Qt dependency, no network access, and no state mutations.
Every result keeps its evidence category and the limits of the observation.
"""
from __future__ import annotations

from typing import Any

SOURCE_LABELS = {
    "local": "Live local diagnostic",
    "imported": "Offline imported evidence",
    "simulation": "Educational simulation",
    "reference": "Educational reference",
}

TITLES = {
    "Dashboard": "System overview",
    "Privacy": "Network privacy diagnostics",
    "MAC Privacy": "MAC privacy profiles",
    "Wi-Fi Audit": "Wireless configuration review",
    "DDoS Defence": "Traffic anomaly learning",
    "Learning Labs": "Cybersecurity learning labs",
    "Router JSON": "Router hardening assessment",
    "Suricata EVE": "Suricata alert review",
    "Zeek JSON": "Zeek connection review",
    "Learning": "Learning centre",
    "Reports": "Assessment reports",
}

ORIGINS = {
    "Dashboard": "local",
    "Privacy": "local",
    "MAC Privacy": "local",
    "Wi-Fi Audit": "local",
    "DDoS Defence": "simulation",
    "Learning Labs": "simulation",
    "Router JSON": "imported",
    "Suricata EVE": "imported",
    "Zeek JSON": "imported",
    "Learning": "reference",
    "Reports": "reference",
}


def _item(label: str, value: Any, status: str = "neutral") -> dict[str, str]:
    return {"label": label, "value": str(value), "status": status}


def _yes_no(value: Any) -> str:
    return "Yes" if value is True else "No" if value is False else "Unknown"


def _limited_findings(value: Any, maximum: int = 12) -> list[dict[str, str]]:
    rows = []
    if isinstance(value, list):
        for item in value[:maximum]:
            if not isinstance(item, dict):
                continue
            severity = str(item.get("severity", item.get("rating", "info"))).lower()
            rows.append({
                "title": str(item.get("code", item.get("finding", item.get("reason", "Observation"))))[:120],
                "detail": str(item.get("recommendation", item.get("description", item.get("reason", ""))))[:600],
                "severity": severity if severity in {"high", "medium", "low", "info", "review"} else "info",
            })
    return rows


def present(title: str, data: dict[str, Any]) -> dict[str, Any]:
    """Return one consistent view model; do not infer protection from services."""
    if not isinstance(data, dict):
        raise ValueError("Expected a diagnostic result object")
    origin = ORIGINS.get(title, "reference")
    summary = "Read-only and local information. No configuration changes."
    caution = "No privacy protection or security outcome has been independently verified."
    cards: list[dict[str, str]] = []
    findings: list[dict[str, str]] = []

    if title == "Dashboard":
        nm = data.get("networkmanager") or {}
        tor = data.get("tor") or {}
        nyx = data.get("nyx") or {}
        proxy = data.get("privoxy") or {}
        cards = [
            _item("NetworkManager", "Available" if nm.get("ready") else "Unavailable",
                  "good" if nm.get("ready") else "neutral"),
            _item("Network devices", nm.get("device_count", "?")),
            _item("Tor installed", _yes_no(tor.get("installed_binary"))),
            _item("Privoxy installed", _yes_no(proxy.get("installed_binary"))),
            _item("Nyx installed", _yes_no(nyx.get("installed_binary"))),
            _item("Network modified", _yes_no(data.get("network_modified")), "good"),
        ]
        summary = "Local component health and service availability."
        caution = "A running Tor or proxy service does not establish anonymous routing."
    elif title == "Privacy":
        socks = data.get("socks5") or {}
        dns = data.get("dns") or {}
        ipv6 = data.get("ipv6") or {}
        cards = [
            _item("SOCKS5 responding", _yes_no(socks.get("responsive"))),
            _item("DNS resolvers", dns.get("resolver_count", "?")),
            _item("DNS manager", dns.get("manager", "Unknown")),
            _item("IPv6 enabled", _yes_no(ipv6.get("enabled"))),
            _item("DNS leak tested", _yes_no(dns.get("leak_tested")), "warning"),
            _item("System protected", "Not verified", "warning"),
        ]
        summary = "Local service and resolver checks, not a live anonymity test."
        caution = "DNS, IP, IPv6 and WebRTC leak protection has not been verified."
    elif title == "MAC Privacy":
        cards = [
            _item("Selected profile", data.get("profile", "Status")),
            _item("Applied", _yes_no(data.get("applied", False)), "warning"),
            _item("Interfaces", data.get("interface_count", "See details")),
            _item("Can apply now", _yes_no(data.get("can_apply", False)), "warning"),
        ]
        summary = "Preview supported NetworkManager privacy concepts."
        caution = "Preview only. No interface address has been changed or hidden."
    elif title == "Wi-Fi Audit":
        count = int(data.get("network_count", 0) or 0)
        findings = _limited_findings(data.get("findings"))
        cards = [
            _item("Connected networks", count),
            _item("Active scans", "No", "good"),
            _item("WPS verified", _yes_no(data.get("wps_verified"))),
            _item("PMF verified", _yes_no(data.get("pmf_verified"))),
        ]
        summary = ("No connected Wi-Fi detected. A VM may expose virtual Ethernet only."
                   if count == 0 else "Read-only checks based on cached connected Wi-Fi data.")
        caution = "This is not a wireless penetration test or a router configuration audit."
    elif title == "DDoS Defence":
        cards = [
            _item("Simulated alerts", data.get("alert_count", 0)),
            _item("Training threshold", data.get("alert_threshold", "?")),
            _item("Data rows", data.get("row_count", "?")),
            _item("Confirmed attack", "No", "good"),
        ]
        findings = _limited_findings(data.get("alerts"))
        summary = "Synthetic traffic counts are used to teach anomaly recognition."
        caution = "No traffic generated. An anomaly is not evidence of a DDoS attack."
    elif title == "Learning Labs":
        lab_list = data.get("labs", [])
        cards = [_item("Available labs", len(lab_list) if isinstance(lab_list, list) else 0),
                 _item("Mode", "Offline")]
        summary = "Guided lessons using synthetic or fictional training data."
        caution = "Learning outcomes are not findings against a real system."
    elif title == "Router JSON":
        findings = _limited_findings(data.get("findings"))
        cards = [
            _item("Findings", data.get("finding_count", len(findings))),
            _item("Connection attempted", "No", "good"),
            _item("Mode", data.get("security_mode", "Offline")),
        ]
        summary = ("Local user-supplied router settings were assessed."
                   if "finding_count" in data else "Choose an authorised router JSON file to review.")
        caution = "Findings describe the provided JSON, not a live check of a router."
    elif title == "Suricata EVE":
        cards = [
            _item("Alerts", data.get("alert_count", 0)),
            _item("Raw IPs exported", "No", "good"),
            _item("Source", "Offline file"),
        ]
        summary = "Read-only classification of previously collected IDS alerts."
        caution = "Suricata alert counts do not establish that a DDoS incident occurred."
    elif title == "Zeek JSON":
        cards = [
            _item("Events", data.get("event_count", 0)),
            _item("Protocols", len(data.get("protocol_counts", {}) or {})),
            _item("Payload bytes", data.get("total_reported_payload_bytes", 0)),
            _item("Confirmed attack", "No", "good"),
        ]
        summary = "Local summary of previously collected Zeek connection logs."
        caution = "Traffic logs require contextual analysis and false-positive review."
    elif title == "Learning":
        lessons = data.get("lessons", [])
        cards = [_item("Lessons", len(lessons) if isinstance(lessons, list) else "Available"),
                 _item("Mode", "Offline")]
        summary = "Education and explanatory content; no active security testing."
    elif title == "Reports":
        cards = [
            _item("Local report", "Available"),
            _item("Protection verified", "No", "warning"),
            _item("Sharing", "Review first"),
        ]
        summary = "Save a private, structured assessment report in HTML."
        caution = "Reports distinguish synthetic examples from local diagnostics."

    return {
        "title": TITLES.get(title, title),
        "provenance": SOURCE_LABELS[origin],
        "provenance_key": origin,
        "summary": summary,
        "caution": caution,
        "cards": cards,
        "findings": findings,
        "technical": data,
    }
