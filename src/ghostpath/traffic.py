"""Read-only OS interface counters for local defensive monitoring."""
from __future__ import annotations

from pathlib import Path


def counters(sys_class_net: Path = Path("/sys/class/net")) -> dict[str, object]:
    rows = []
    if sys_class_net.is_dir():
        for folder in sorted(sys_class_net.iterdir()):
            if not folder.is_dir() or folder.name == "lo":
                continue
            stats = folder / "statistics"
            try:
                row = {"interface": folder.name}
                for name in ("rx_bytes", "tx_bytes", "rx_packets", "tx_packets", "rx_dropped", "tx_dropped"):
                    row[name] = int((stats / name).read_text(encoding="utf-8").strip())
                rows.append(row)
            except (OSError, ValueError):
                continue
    return {
        "source": "read-only Linux sysfs counters",
        "interfaces": rows,
        "rate_calculated": False,
        "note": "Counters are cumulative, not live packet rates or evidence of an attack.",
    }
