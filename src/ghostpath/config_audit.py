"""Offline owned-router Wi-Fi configuration assessment; no network activity."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def audit_settings(settings: dict[str, Any]) -> dict[str, object]:
    if not isinstance(settings, dict):
        raise ValueError("Expected a JSON object with router security settings")
    security = str(settings.get("security", "unknown")).strip().upper()
    wps = settings.get("wps_enabled")
    pmf = str(settings.get("pmf", "unknown")).strip().lower()
    guest = settings.get("guest_isolation")
    findings: list[dict[str, str]] = []

    def flag(severity: str, code: str, recommendation: str) -> None:
        findings.append({"severity": severity, "code": code, "recommendation": recommendation})

    if security in ("OPEN", "NONE", "WEP", "WPA", "WPA1"):
        flag("high", "legacy_wireless_security", "Prefer WPA3 or WPA2-AES on your owned router.")
    elif security == "UNKNOWN":
        flag("review", "security_unknown", "Check the authentication mode in your access point settings.")
    elif "WPA2" in security and "WPA3" not in security:
        flag("medium", "wpa2_only", "Consider WPA3 if supported by all required clients.")
    elif "WPA3" not in security and "WPA2" not in security and "ENTERPRISE" not in security:
        flag("review", "unrecognised_mode", "Verify encryption compatibility and configuration.")
    if wps is True:
        flag("medium", "wps_enabled", "Disable WPS when it is not required.")
    if pmf in ("disabled", "off", "none"):
        flag("medium", "pmf_disabled", "Enable protected management frames where supported.")
    if guest is False:
        flag("low", "guest_isolation", "Consider isolating guest devices from private networks.")
    return {
        "method": "offline_owned_router_settings",
        "security_mode": security,
        "findings": findings,
        "finding_count": len(findings),
        "network_identifiers_excluded": True,
        "any_connection_attempted": False,
        "limitations": "User-supplied settings only; no radio, password or access testing performed.",
    }


def audit_file(path: Path) -> dict[str, object]:
    try:
        if not path.is_file() or path.stat().st_size > 256_000:
            raise ValueError("Provide a JSON settings file no larger than 256 KB")
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid UTF-8 JSON router settings file") from exc
    return audit_settings(obj)
