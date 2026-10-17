"""Offline, bounded security event analytics for educational DDoS defence.

No socket opening, packet crafting or traffic generation of any kind.
"""
from __future__ import annotations

import csv
import io
import statistics
from pathlib import Path

MAX_BYTES = 1_000_000
MAX_ROWS = 2_000
MAX_COUNT = 10_000_000


def example_events(scenario: str = "surge") -> list[dict[str, int]]:
    if scenario not in {"normal", "surge", "busy"}:
        raise ValueError("Unknown offline scenario")
    events = []
    for n in range(24):
        count = 95 + ((n * 19) % 23)
        if scenario == "surge" and 16 <= n < 20:
            count += 650
        if scenario == "busy" and 12 <= n < 18:
            count += 130
        events.append({"minute": n, "requests": count, "errors": count // 20})
    return events


def parse_csv(path: Path) -> list[dict[str, int]]:
    """Read a local CSV with strict schema and resource limits."""
    if not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise ValueError("CSV must exist and be at most 1 MB")
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeError as exc:
        raise ValueError("CSV must use UTF-8") from exc
    rows = csv.DictReader(io.StringIO(text))
    if rows.fieldnames != ["minute", "requests", "errors"]:
        raise ValueError("Required CSV columns: minute,requests,errors")
    events = []
    last_minute = -1
    for row in rows:
        if len(events) >= MAX_ROWS:
            raise ValueError("CSV exceeds the 2,000-row safety limit")
        try:
            minute = int(row["minute"])
            requests = int(row["requests"])
            errors = int(row["errors"])
        except (ValueError, TypeError) as exc:
            raise ValueError("Expected nonnegative integer data") from exc
        if (minute <= last_minute or minute < 0 or requests < 0
                or requests > MAX_COUNT or not 0 <= errors <= requests):
            raise ValueError("CSV must have increasing minutes and valid bounded counts")
        last_minute = minute
        events.append({"minute": minute, "requests": requests, "errors": errors})
    if not events:
        raise ValueError("CSV has no data rows")
    return events


def analyze(events: list[dict[str, int]]) -> dict[str, object]:
    if not 3 <= len(events) <= MAX_ROWS:
        raise ValueError("Expected 3 to 2,000 offline event rows")
    for item in events:
        if not all(k in item and isinstance(item[k], int) for k in ("minute", "requests", "errors")):
            raise ValueError("Invalid event row")
        if not 0 <= item["errors"] <= item["requests"] <= MAX_COUNT:
            raise ValueError("Invalid event counts")
    # Use a fixed early baseline. This is a learning heuristic, not real-time detection.
    base_values = [item["requests"] for item in events[:min(8, len(events))]]
    baseline = statistics.median(base_values)
    threshold = max(250.0, baseline * 3.0)
    flagged = []
    for item in events:
        if item["requests"] > threshold:
            flagged.append({
                "minute": item["minute"],
                "requests": item["requests"],
                "reason": "Volume exceeds training threshold",
            })
    return {
        "source": "offline event counts only",
        "row_count": len(events),
        "baseline_median": baseline,
        "alert_threshold": threshold,
        "alerts": flagged,
        "alert_count": len(flagged),
        "classification": "anomaly" if flagged else "no volume anomaly",
        "confirmed_ddos": False,
        "interpretation": "Traffic spikes can be legitimate; review capacity, error rates and source logs.",
        "mitigation": [
            "Verify service health and identify the affected application.",
            "Check upstream WAF/CDN/provider protections and rate limits.",
            "Preserve relevant logs and review false positives before blocking.",
            "Escalate suspected incidents to the network or hosting provider.",
        ],
    }
