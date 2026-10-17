"""Offline Suricata EVE alert summary, excluding IPs and payload data."""
from __future__ import annotations

import json
from pathlib import Path

MAX_EVE_BYTES = 8_000_000
MAX_EVENTS = 50_000


def summarize_eve(path: Path) -> dict[str, object]:
    if not path.is_file() or path.stat().st_size > MAX_EVE_BYTES:
        raise ValueError("Provide a local EVE JSONL file no larger than 8 MB")
    severities: dict[str, int] = {}
    categories: dict[str, int] = {}
    count = 0
    try:
        with path.open("r", encoding="utf-8") as file:
            for number, line in enumerate(file):
                if number >= MAX_EVENTS:
                    raise ValueError("EVE input exceeds 50,000 events")
                event = json.loads(line)
                if not isinstance(event, dict) or event.get("event_type") != "alert":
                    continue
                alert = event.get("alert")
                if not isinstance(alert, dict):
                    continue
                count += 1
                sev = str(alert.get("severity", "unknown"))[:12]
                category = str(alert.get("category", "unknown"))[:100]
                severities[sev] = severities.get(sev, 0) + 1
                categories[category] = categories.get(category, 0) + 1
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError("EVE input must be valid UTF-8 JSONL") from exc
    return {
        "analysis_type": "offline_suricata_eve",
        "alert_count": count,
        "severity_counts": severities,
        "category_counts": categories,
        "source_addresses_included": False,
        "traffic_generated": False,
        "warning": "Alert counts are not proof of a DDoS attack.",
    }
