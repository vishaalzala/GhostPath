"""Constrained command execution for diagnostics.

No shell, no dynamic user-provided executable, bounded execution time.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass

ALLOWED_EXECUTABLES = frozenset(
    {"systemctl", "nmcli", "tor", "privoxy", "nyx"}
)


@dataclass(frozen=True)
class Result:
    available: bool
    returncode: int | None
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.available and self.returncode == 0


def run_readonly(args: list[str], timeout: float = 4.0) -> Result:
    if not args or args[0] not in ALLOWED_EXECUTABLES:
        raise ValueError("Executable is not allowed")
    # Only the explicitly supported read-only argument shapes are accepted.
    commands = {
        ("systemctl", "show", "--property=LoadState,ActiveState,SubState", "tor@default.service"),
        ("systemctl", "show", "--property=LoadState,ActiveState,SubState", "tor.service"),
        ("systemctl", "show", "--property=LoadState,ActiveState,SubState", "privoxy.service"),
        ("nmcli", "-t", "-f", "DEVICE,TYPE,STATE", "device", "status"),
        ("nmcli", "-t", "-f", "IN-USE,SSID,SECURITY,SIGNAL", "device", "wifi", "list", "--rescan", "no"),
        ("tor", "--version"),
        ("privoxy", "--version"),
        ("nyx", "--version"),
    }
    if tuple(args) not in commands:
        raise ValueError("Only approved read-only diagnostics are supported")
    try:
        completed = subprocess.run(
            args, check=False, capture_output=True, text=True, timeout=timeout,
            shell=False, env={"PATH": "/usr/sbin:/usr/bin:/sbin:/bin", "LC_ALL": "C"},
        )
        return Result(True, completed.returncode, completed.stdout[:8000], completed.stderr[:3000])
    except FileNotFoundError:
        return Result(False, None, "", "Command not installed")
    except subprocess.TimeoutExpired:
        return Result(True, None, "", "Diagnostic timed out")
    except OSError:
        return Result(False, None, "", "Diagnostic cannot run")
