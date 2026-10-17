"""Non-invasive Wi-Fi posture review for an authorised connected network.

No active discovery, disconnection, credential attacks or packet transmission.
"""
from __future__ import annotations

from .network import connected_wifi


def assess_security(security: str) -> dict[str, object]:
    value = security.upper().strip()
    if not value or value in {"--", "OPEN", "NONE"}:
        return {"rating": "high", "finding": "Unencrypted wireless network",
                "recommendation": "Use WPA3-Personal or WPA2-AES where WPA3 is unavailable."}
    if "WEP" in value or "WPA1" in value or "TKIP" in value:
        return {"rating": "high", "finding": "Legacy wireless protection indicated",
                "recommendation": "Disable WEP/WPA1/TKIP and update the access point configuration."}
    if "WPA3" in value or "SAE" in value:
        return {"rating": "informational", "finding": "Modern security mode advertised",
                "recommendation": "Review access-point updates, passwords, PMF and guest isolation."}
    if "WPA2" in value or "802.1X" in value or "WPA" in value:
        return {"rating": "review", "finding": "Protected mode advertised, configuration unknown",
                "recommendation": "Verify AES/CCMP, firmware updates and protected management frames."}
    return {"rating": "unknown", "finding": "Could not classify the advertised security string",
            "recommendation": "Inspect router settings with the owner's permission."}


def wifi_audit(cached: dict[str, object] | None = None) -> dict[str, object]:
    cached = cached if cached is not None else connected_wifi()
    findings = []
    for index, access_point in enumerate(cached.get("connected", []), start=1):
        item = assess_security(str(access_point.get("security", "")))
        findings.append({"network_number": index, "advertised_security": str(
            access_point.get("security", "unknown")), **item})
    return {
        "network_count": len(findings), "findings": findings,
        "identifiers_redacted": True, "active_scans": False,
        "pmf_verified": False, "wps_verified": False,
        "note": "Reports advertised settings from cache, not a wireless penetration test.",
    }
