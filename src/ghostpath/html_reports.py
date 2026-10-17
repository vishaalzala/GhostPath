"""Readable offline HTML reports, safely escaped and saved with private permissions.

The report explicitly separates local observations, imported evidence, and
educational examples. No remote dependencies, scripts, or automatic uploads.
"""
from __future__ import annotations

import html
import json
import os
from pathlib import Path
from typing import Any

SENSITIVE_KEYS = frozenset({
    "password", "passphrase", "secret", "token", "access_token", "api_key",
    "private_key", "ssid", "bssid", "mac_address", "mac", "hostname",
    "username", "src_ip", "dst_ip", "source_ip", "destination_ip",
    "ip_address", "dns_servers", "nameservers", "id.orig_h", "id.resp_h",
})


def _safe(value: object) -> str:
    return html.escape(str(value), quote=True)


def _redact(value: Any, depth: int = 0) -> Any:
    """Strip known identifier/secret fields before embedding technical details."""
    if depth > 18:
        return "[Nested data omitted]"
    if isinstance(value, dict):
        return {
            str(key)[:120]: _redact(item, depth + 1)
            for key, item in value.items()
            if str(key).strip().lower() not in SENSITIVE_KEYS
        }
    if isinstance(value, list):
        return [_redact(item, depth + 1) for item in value[:400]]
    if isinstance(value, str):
        return value[:2500]
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    return str(value)[:120]


def _table(rows: list[tuple[str, object]]) -> str:
    return "<table><tbody>" + "".join(
        "<tr><th scope='row'>" + _safe(key) + "</th><td>" +
        _safe(value) + "</td></tr>" for key, value in rows
    ) + "</tbody></table>"


def _section(title: str, source: str, intro: str, rows: list[tuple[str, object]]) -> str:
    return (
        "<section class='panel'><div class='eyebrow'>" + _safe(source) + "</div>"
        "<h2>" + _safe(title) + "</h2>"
        "<p>" + _safe(intro) + "</p>" + _table(rows) + "</section>"
    )


def render_html_report(data: dict[str, object]) -> str:
    """Build a readable, self-contained report, no JavaScript or external requests."""
    if not isinstance(data, dict):
        raise ValueError("Assessment report must be a mapping")
    clean = _redact(data)
    dns = clean.get("dns") or {}
    mac = clean.get("mac_plan_example") or {}
    traffic = clean.get("offline_training_example") or {}
    wifi = clean.get("wifi_example") or {}
    imported = clean.get("offline_imported_evidence")
    if not all(isinstance(x, dict) for x in (dns, mac, traffic, wifi)):
        raise ValueError("Unexpected assessment report schema")

    protected = bool(clean.get("system_protection_verified", False))
    # Never infer verified protection from the presence of Tor, DNS or proxies.
    protection_text = "Not verified" if not protected else "Claim in source data — independently verify"
    alerts = int(traffic.get("alert_count", 0) or 0)
    resolver_count = dns.get("resolver_count", "Unknown")
    available_labs = clean.get("available_labs", "Unknown")

    sections = [
        _section(
            "Local DNS diagnostic", "LIVE LOCAL DIAGNOSTIC",
            "Resolver configuration was inspected. This is not a DNS leak test.",
            [
                ("Resolver count", resolver_count),
                ("Resolver manager", dns.get("manager", "Unknown")),
                ("Local stub resolver", "Yes" if dns.get("local_resolver") else "No / unknown"),
                ("DNS leak tested", "No"),
                ("Finding", dns.get("warning", "No leak claim can be made")),
            ],
        ),
        _section(
            "MAC privacy profile example", "EDUCATIONAL PREVIEW",
            "This describes a supported concept and does not change an interface.",
            [
                ("Profile", mac.get("profile", "Unknown")),
                ("NetworkManager mode", mac.get("networkmanager_mode", "Unknown")),
                ("Applied to device", "No"),
                ("Compatibility", "Not yet tested on hardware"),
                ("Privacy limitation", mac.get("tradeoff", "MACs remain observable on a local link")),
            ],
        ),
        _section(
            "Wireless security example", "EDUCATIONAL SIMULATION",
            "This example is not a live security finding about your router.",
            [
                ("Assessment", wifi.get("rating", "Unknown")),
                ("Example finding", wifi.get("finding", "None")),
                ("Guidance", wifi.get("recommendation", "Review authorised router settings")),
            ],
        ),
        _section(
            "Traffic anomaly learning", "EDUCATIONAL SIMULATION",
            "Deterministic offline traffic counts; no target was contacted.",
            [
                ("Baseline events", traffic.get("baseline_median", "Unknown")),
                ("Training threshold", traffic.get("alert_threshold", "Unknown")),
                ("Illustrative alerts", alerts),
                ("Classification", traffic.get("classification", "Unknown")),
                ("Confirmed DDoS", "No"),
                ("Interpretation", traffic.get("interpretation", "Investigate false positives")),
            ],
        ),
    ]

    if isinstance(imported, dict):
        values = imported.get("results")
        if not isinstance(values, dict):
            values = {}
        source = str(imported.get("source", "Authorised offline file"))
        overview = []
        for key in (
            "finding_count", "alert_count", "event_count", "total_reported_payload_bytes",
            "analysis_type", "security_mode", "confirmed_attack",
        ):
            if key in values:
                overview.append((key.replace("_", " ").title(), values[key]))
        sections.append(_section(
            source, "OFFLINE IMPORTED EVIDENCE",
            "An authorised file was imported. These findings are based on supplied data, "
            "not on a live network test.",
            overview or [("Result", "File analysed; see technical details")],
        ))

    caution = (
        "This document combines local configuration observations and clearly marked "
        "training examples. No system-wide Tor routing, DNS/IP leak prevention, "
        "active MAC randomisation or real-world DDoS incident has been verified."
    )
    technical = _safe(json.dumps(clean, indent=2, sort_keys=True, ensure_ascii=True))
    tiles = [
        ("Protection status", protection_text),
        ("Local DNS resolvers", resolver_count),
        ("Synthetic anomaly alerts", alerts),
        ("Offline learning labs", available_labs),
    ]
    tiles_html = "".join(
        "<div class='tile'><small>" + _safe(key) + "</small><strong>" + _safe(val) +
        "</strong></div>" for key, val in tiles
    )
    body = "".join(sections)
    stamp = _safe(clean.get("created_at", "Time not supplied"))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'none'; connect-src 'none'; script-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>GhostPath | Defensive Assessment Report</title>
<style>
:root {{color-scheme:light;}}
* {{box-sizing:border-box;}}
body {{background:#eef3f8;color:#193047;font:15px/1.6 system-ui,-apple-system,Segoe UI,sans-serif;margin:0;}}
main {{width:min(1050px,calc(100% - 40px));margin:0 auto;padding:36px 0 60px;}}
.hero {{background:#12253b;color:white;padding:28px 32px;border-radius:18px;}}
.hero p {{color:#c1d5e4;margin:5px 0;}}
.eyebrow {{font-weight:800;font-size:11px;letter-spacing:.11em;color:#187b8a;}}
.hero .eyebrow {{color:#8bd9d9;}}
h1 {{font-size:29px;margin:4px 0 12px;line-height:1.2;}}
h2 {{font-size:19px;margin:3px 0 8px;line-height:1.35;}}
p {{margin:8px 0 15px;color:#52657b;}}
.notice {{border:1px solid #d3af65;background:#fff6dc;border-radius:10px;padding:14px 18px;margin:22px 0;}}
.notice strong {{display:block;color:#795016;}}
.tiles {{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:20px 0;}}
.tile,.panel {{background:white;border:1px solid #d9e5ef;border-radius:12px;}}
.tile {{padding:18px;}}
.tile small {{display:block;color:#586b7f;font-weight:650;}}
.tile strong {{display:block;margin-top:6px;font-size:19px;color:#17334d;overflow-wrap:anywhere;}}
.panel {{padding:23px 26px;margin:16px 0;page-break-inside:avoid;}}
table {{border-collapse:collapse;width:100%;text-align:left;}}
th,td {{padding:9px 8px;border-bottom:1px solid #e3eaf2;vertical-align:top;overflow-wrap:anywhere;}}
th {{width:35%;font-weight:650;color:#4c6479;}}
td {{color:#203449;}}
details {{background:white;border:1px solid #d9e5ef;border-radius:12px;padding:17px;margin-top:20px;}}
summary {{cursor:pointer;font-weight:700;}}
pre {{white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.55 ui-monospace,Consolas,monospace;}}
footer {{font-size:12px;color:#6c7e8d;margin-top:20px;}}
@media(max-width:720px) {{.tiles{{grid-template-columns:repeat(2,minmax(0,1fr));}}.hero{{padding:22px;}}th{{width:42%;}}}}
@media print {{body{{background:white;}}main{{width:100%;padding:0;}}.hero{{border-radius:0;}}.panel{{break-inside:avoid;}}details{{display:none;}}}}
</style></head>
<body><main>
<header class="hero"><div class="eyebrow">GHOSTPATH · PRIVATE LOCAL REPORT</div>
<h1>Defensive Security Assessment</h1>
<p>Read-only diagnostics, imported evidence and educational examples, explicitly separated.</p>
<p>Generated: {stamp}</p></header>
<div class="notice"><strong>Protection not verified</strong>{_safe(caution)}</div>
<div class="tiles">{tiles_html}</div>
{body}
<details><summary>Technical details · redacted JSON</summary><pre>{technical}</pre></details>
<footer>GhostPath v2 development alpha · Educational use on owned or authorised systems.
This file was created locally and contains no scripts, trackers or external resources.
Review the contents before sharing.</footer>
</main></body></html>"""


def save_html_report(data: dict[str, object], path: Path) -> dict[str, object]:
    path = Path(path)
    if path.suffix.lower() not in (".html", ".htm"):
        raise ValueError("HTML report path must end with .html or .htm")
    text = render_html_report(data)
    if len(text.encode("utf-8")) > 1_000_000:
        raise ValueError("Report exceeds the 1 MB maximum")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(str(path), flags, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        path.unlink(missing_ok=True)
        raise
    return {
        "created": True,
        "location": str(path),
        "private_permissions": True,
        "note": "Readable local HTML report created; review before sharing. Print to PDF in a browser.",
    }
