"""Bounded, offline Zeek JSON connection-log summary.

No packet capture, network connections, process execution, or sensitive
address export. A Zeek log must be collected with permission beforehand.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

MAX_FILE_BYTES = 8_000_000
MAX_EVENTS = 50_000
MAX_LINE_LENGTH = 65_536


def summarize_zeek(path: Path) -> dict[str, object]:
    """Summarise an authorised Zeek JSON conn.log; exclude IPs and hostnames."""
    path = Path(path)
    if not path.is_file() or path.suffix.lower() not in {".jsonl", ".json", ".log"}:
        raise ValueError("Provide an existing Zeek JSONL (.json/.jsonl/.log) file")
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("Zeek JSONL input exceeds the 8 MB limit")

    protocols: Counter[str] = Counter()
    states: Counter[str] = Counter()
    hours: Counter[str] = Counter()
    byte_total = 0
    records = 0
    try:
        with path.open("r", encoding="utf-8-sig") as stream:
            for line in stream:
                if len(line) > MAX_LINE_LENGTH:
                    raise ValueError("Zeek record exceeds the maximum line length")
                if not line.strip():
                    continue
                records += 1
                if records > MAX_EVENTS:
                    raise ValueError("Zeek JSONL input exceeds the 50,000-record limit")
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise ValueError("Every Zeek log entry must be a JSON object")
                raw_ts = record.get("ts")
                if isinstance(raw_ts, bool) or not isinstance(raw_ts, (int, float)):
                    raise ValueError("Zeek JSON entry is missing a numeric ts value")
                timestamp = float(raw_ts)
                if not math.isfinite(timestamp):
                    raise ValueError("Zeek log timestamp must be finite")
                try:
                    hour = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime(
                        "%Y-%m-%dT%H:00:00Z"
                    )
                except (OverflowError, OSError, ValueError) as exc:
                    raise ValueError("Zeek timestamp is out of range") from exc
                protocols[str(record.get("proto", "unknown"))[:24].lower()] += 1
                states[str(record.get("conn_state", "unknown"))[:24]] += 1
                hours[hour] += 1
                for key in ("orig_bytes", "resp_bytes"):
                    value = record.get(key)
                    if value is None:
                        continue
                    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                        continue
                    byte_total += min(value, 2**63 - 1)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("Zeek log must be valid UTF-8 newline-delimited JSON") from exc

    if records == 0:
        raise ValueError("Zeek log contains no JSON events")

    return {
        "analysis_type": "offline_zeek_json_summary",
        "event_count": records,
        "total_reported_payload_bytes": byte_total,
        "protocol_counts": dict(protocols.most_common(12)),
        "connection_state_counts": dict(states.most_common(24)),
        "hourly_event_counts": [
            {"utc_hour": hour, "events": count} for hour, count in sorted(hours.items())
        ],
        "source_addresses_included": False,
        "hostnames_included": False,
        "network_traffic_generated": False,
        "confirmed_attack": False,
        "warning": (
            "Events describe observed connections, not attack intent. "
            "Log volume depends on collection settings; investigate false positives."
        ),
    }
