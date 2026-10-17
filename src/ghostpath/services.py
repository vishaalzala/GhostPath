"""Tor and HTTP proxy diagnostics, no service mutation."""
from __future__ import annotations

from .core.runner import run_readonly


def _unit_status(unit: str) -> dict[str, str]:
    result = run_readonly(["systemctl", "show", "--property=LoadState,ActiveState,SubState", unit])
    if not result.ok:
        return {"unit": unit, "load": "unknown", "active": "unknown", "sub": "unknown"}
    parts = dict(
        line.split("=", 1) for line in result.stdout.splitlines() if "=" in line
    )
    return {
        "unit": unit,
        "load": parts.get("LoadState", "unknown"),
        "active": parts.get("ActiveState", "unknown"),
        "sub": parts.get("SubState", "unknown"),
    }


def tor_status() -> dict[str, object]:
    units = [_unit_status("tor@default.service"), _unit_status("tor.service")]
    valid = [u for u in units if u["load"] == "loaded"]
    # tor.service may be only a wrapper; a loaded, active instance is preferred.
    candidate = valid[0] if valid else None
    return {
        "installed_binary": run_readonly(["tor", "--version"]).available,
        "units": units,
        "selected_unit": candidate["unit"] if candidate else None,
        "service_active": bool(candidate and candidate["active"] == "active"),
        "routing_verified": False,
        "warning": "A running Tor service does not prove application traffic uses Tor.",
    }


def proxy_status() -> dict[str, object]:
    unit = _unit_status("privoxy.service")
    return {
        "installed_binary": run_readonly(["privoxy", "--version"]).available,
        "unit": unit,
        "proxy_verified": False,
        "warning": "A running proxy does not prove the application is configured to use it.",
    }


def nyx_status() -> dict[str, object]:
    result = run_readonly(["nyx", "--version"])
    return {"installed_binary": result.available, "available": result.ok}
