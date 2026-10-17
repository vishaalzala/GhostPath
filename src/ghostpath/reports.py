"""Explicit, local-only, privacy-reduced assessment exports."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from .defense import analyze, example_events
from .labs import list_labs
from .mac_privacy import plan
from .privacy import dns_status
from .wifi_audit import assess_security

REPORT_SCHEMA = 1


def build_report() -> dict[str, object]:
    """No hostnames, identifiers, MAC/SSID, passwords, IPs or live packets."""
    return {
        "schema": REPORT_SCHEMA,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "report_kind": "educational-local-assessment",
        "offline_training_example": analyze(example_events("surge")),
        "dns": dns_status(),
        "wifi_example": assess_security("WPA2"),
        "mac_plan_example": plan("stable"),
        "available_labs": len(list_labs()["labs"]),
        "system_protection_verified": False,
        "warning": "Examples and limited local metadata are not proof of security or anonymity.",
    }


def save_report(data: dict[str, object], path: Path) -> dict[str, object]:
    """Create a NEW private report, never overwrite or follow a final symlink."""
    if not path.name.endswith(".json"):
        raise ValueError("Report path must end with .json")
    serialized = (json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    if len(serialized) > 1_000_000:
        raise ValueError("Report exceeds size limit")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(str(path), flags, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as file:
            file.write(serialized)
            file.flush()
            os.fsync(file.fileno())
    except BaseException:
        path.unlink(missing_ok=True)
        raise
    return {
        "created": True,
        "location": str(path),
        "private_permissions": True,
        "note": "Please review and redact further before sharing publicly.",
    }
