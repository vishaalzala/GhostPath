"""Privacy-preserving, bounded OFFLINE Suricata/Zeek JSONL event analysis.

This module reads existing, authorised event files; it cannot capture,
generate, amplify or send network traffic.
"""
from __future__ import annotations

import hashlib
import json
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_EVENTS = 20000
MAX_LINE_CHARS = 65536
ALLOWED_FORMATS = frozenset(("auto", "eve", "zeek"))


def _timestamp(value: object) -> datetime:
    try:
        if isinstance(value, (int, float)):
            dt = datetime.fromtimestamp(float(value), tz=timezone.utc)
        else:
            text = str(value).strip()
            if not text:
                raise ValueError("timestamp missing")
            if text.replace(".", "", 1).isdigit():
                dt = datetime.fromtimestamp(float(text), tz=timezone.utc)
            else:
                dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (ValueError, OverflowError, OSError) as exc:
        raise ValueError("Unsupported event timestamp") from exc


def _event(raw: dict[str, object], source_format: str) -> dict[str, object]:
    if source_format == "eve":
        when = raw.get("timestamp")
        src = raw.get("src_ip", "")
        protocol = raw.get("proto", "unknown")
        flow = raw.get("flow", {})
        if not isinstance(flow, dict):
            flow = {}
        is_alert = raw.get("event_type") == "alert"
        try:
            byte_count = int(flow.get("bytes_toserver", 0)) + int(flow.get("bytes_toclient", 0))
        except (TypeError, ValueError):
            byte_count = 0
    else:
        when = raw.get("ts")
        src = raw.get("id.orig_h", "")
        protocol = raw.get("proto", "unknown")
        is_alert = raw.get("note") is not None or raw.get("_path") == "notice"
        try:
            byte_count = int(raw.get("orig_bytes") or 0) + int(raw.get("resp_bytes") or 0)
        except (TypeError, ValueError):
            byte_count = 0
    timestamp = _timestamp(when)
    anonymous_id = hashlib.sha256(str(src).encode("utf-8")[:512]).hexdigest()[:10]
    return {
        "minute": timestamp.strftime("%Y-%m-%dT%H:%M:00Z"),
        "anonymous_source_id": anonymous_id,
        "protocol": str(protocol)[:24].upper(),
        "bytes": max(0, min(byte_count, 2**63 - 1)),
        "alert": bool(is_alert),
    }


def analyze_event_file(path: Path, source_format: str = "auto") -> dict[str, object]:
    """Analyse EVE or Zeek line-delimited JSON, never returning raw addresses."""
    if source_format not in ALLOWED_FORMATS:
        raise ValueError("Format must be auto, eve, or zeek")
    path = Path(path)
    if not path.is_file() or path.suffix.lower() not in {".jsonl", ".json", ".log"}:
        raise ValueError("Expected an existing local JSONL (.jsonl/.json/.log) file")
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("Offline log exceeds the 8 MiB limit")
    buckets: dict[str, dict[str, int]] = defaultdict(lambda: {"events": 0, "bytes": 0, "alerts": 0})
    protocol_counts: Counter[str] = Counter()
    anonymous_sources: Counter[str] = Counter()
    event_count = 0
    inferred_format = source_format
    try:
        with path.open("r", encoding="utf-8-sig") as stream:
            for line in stream:
                if len(line) > MAX_LINE_CHARS:
                    raise ValueError("Event line exceeds allowed length")
                if not line.strip():
                    continue
                event_count += 1
                if event_count > MAX_EVENTS:
                    raise ValueError("Event count exceeds the 20,000-event limit")
                raw = json.loads(line)
                if not isinstance(raw, dict):
                    raise ValueError("Every line must contain a JSON object")
                this_format = source_format
                if source_format == "auto":
                    this_format = "eve" if "event_type" in raw or "timestamp" in raw else "zeek"
                    if inferred_format == "auto":
                        inferred_format = this_format
                    elif inferred_format != this_format:
                        raise ValueError("Mixed EVE and Zeek input is not supported")
                event = _event(raw, this_format)
                entry = buckets[str(event["minute"])]
                entry["events"] += 1
                entry["bytes"] += int(event["bytes"])
                entry["alerts"] += int(event["alert"])
                protocol_counts[str(event["protocol"])] += 1
                anonymous_sources[str(event["anonymous_source_id"])] += 1
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("Log must contain valid UTF-8 line-delimited JSON objects") from exc
    if not event_count:
        raise ValueError("Log contains no supported events")
    counts = [bucket["events"] for bucket in buckets.values()]
    baseline = statistics.median(counts)
    threshold = max(20, baseline * 3)
    anomalies = [
        {"minute": minute, "events": value["events"], "reason": "Volume above simple training baseline"}
        for minute, value in sorted(buckets.items())
        if value["events"] > threshold
    ]
    return {
        "format": inferred_format,
        "source": "offline authorised security event log",
        "event_count": event_count,
        "minutes_observed": len(buckets),
        "per_minute": [{"minute": minute, **value} for minute, value in sorted(buckets.items())],
        "protocol_counts": dict(protocol_counts.most_common(12)),
        "anonymous_source_counts": [
            {"id": src, "events": count} for src, count in anonymous_sources.most_common(5)
        ],
        "anomalies": anomalies,
        "signature_alert_events": sum(value["alerts"] for value in buckets.values()),
        "confirmed_ddos": False,
        "raw_addresses_included": False,
        "network_sent": False,
        "caution": (
            "Log event counts may reflect logging configuration, not request rates. "
            "Anomalies and alerts require corroboration and false-positive review."
        ),
    }
