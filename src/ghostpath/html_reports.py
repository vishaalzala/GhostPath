"""Escaped HTML report export with exclusive private-file creation."""
from __future__ import annotations

import html
import json
import os
from pathlib import Path


def save_html_report(data: dict[str, object], path: Path) -> dict[str, object]:
    if path.suffix.lower() not in (".html", ".htm"):
        raise ValueError("HTML report path must end with .html or .htm")
    safe = html.escape(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))
    text = (
        "<!doctype html><html lang='en'><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<title>GhostPath Defensive Assessment</title>"
        "<style>body{font:16px system-ui;max-width:960px;margin:2rem auto;padding:1rem}"
        "pre{background:#f4f5f7;padding:1.5rem;border-radius:8px;"
        "overflow-wrap:anywhere;white-space:pre-wrap}</style>"
        "<h1>GhostPath — Defensive Assessment</h1>"
        "<p>Educational and local findings only. No privacy guarantees.</p>"
        f"<pre>{safe}</pre></html>"
    )
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
        "note": "Review before sharing. HTML can be printed to PDF in a browser.",
    }
