"""Headless Qt startup test: validate tabs without changing system settings."""
from __future__ import annotations

import os
import sys

if os.environ.get("QT_QPA_PLATFORM") != "offscreen":
    raise SystemExit("Only run this CI smoke test with QT_QPA_PLATFORM=offscreen")

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QTabWidget
from ghostpath.gui import main as run_gui

app = QApplication.instance() or QApplication(sys.argv[:1])
result = {"passed": False}


def check() -> None:
    tabs = [widget for widget in QApplication.allWidgets() if isinstance(widget, QTabWidget)]
    if not tabs:
        print("No GhostPath tab view found", file=sys.stderr)
    else:
        titles = {tab.tabText(i) for tab in tabs for i in range(tab.count())}
        needed = {"Dashboard", "Privacy", "MAC Privacy", "Wi-Fi Audit", "DDoS Defence", "Router JSON", "Suricata EVE", "Zeek JSON", "Reports"}
        if needed.issubset(titles):
            print("GUI smoke passed:", sorted(titles))
            result["passed"] = True
        else:
            print(f"Missing GUI sections: {sorted(needed - titles)}", file=sys.stderr)
    app.quit()


QTimer.singleShot(500, check)
QTimer.singleShot(5000, app.quit)
rc = run_gui()
if rc != 0 or not result["passed"]:
    raise SystemExit(1)
