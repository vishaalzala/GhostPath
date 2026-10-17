"""Headless Qt integration check for GhostPath's redesigned desktop UI."""
from __future__ import annotations

import os
import sys

if os.environ.get("QT_QPA_PLATFORM") != "offscreen":
    raise SystemExit("GUI CI smoke requires QT_QPA_PLATFORM=offscreen")

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QTabWidget, QPushButton, QLabel
from ghostpath.gui import main as run_gui

app = QApplication.instance() or QApplication(sys.argv[:1])
result = {"passed": False}


def check() -> None:
    widgets = QApplication.allWidgets()
    tab_widgets = [widget for widget in widgets if isinstance(widget, QTabWidget)]
    needed = {
        "Dashboard", "Privacy", "MAC Privacy", "Wi-Fi Audit", "DDoS Defence",
        "Learning Labs", "Router JSON", "Suricata EVE", "Zeek JSON",
        "Learning", "Reports",
    }
    actual = {
        tab.tabText(index)
        for tab in tab_widgets
        for index in range(tab.count())
    }
    detail_controls = [
        widget for widget in widgets
        if isinstance(widget, QPushButton) and widget.objectName() == "detailsToggle"
    ]
    has_banner = any(
        isinstance(widget, QLabel) and widget.objectName() == "statusChip"
        for widget in widgets
    )
    if not needed.issubset(actual):
        print(f"Missing tabs: {sorted(needed - actual)}", file=sys.stderr)
    elif len(detail_controls) < len(needed):
        print("Expected technical-details toggles for all panels", file=sys.stderr)
    elif not has_banner:
        print("Missing alpha/read-only security warning", file=sys.stderr)
    else:
        first = detail_controls[0]
        first.setChecked(True)
        first.setChecked(False)
        print("Redesigned GUI passed: cards layout, tab navigation and details toggles")
        result["passed"] = True
    app.quit()


QTimer.singleShot(850, check)
QTimer.singleShot(9000, app.quit)
rc = run_gui()
if rc != 0 or not result["passed"]:
    raise SystemExit(1)
