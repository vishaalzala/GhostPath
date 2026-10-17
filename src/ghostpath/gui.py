"""GhostPath v2 desktop: accessible summaries with opt-in technical JSON.

Local/offline only. No automatic network changes or unverified protection claims.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from .config_audit import audit_file as audit_router_file
from .defense import analyze, example_events
from .diagnostics import doctor
from .eve import summarize_eve
from .html_reports import save_html_report
from .labs import list_labs, run_lab
from .lessons import list_lessons, read_lesson
from .mac_privacy import plan, status as mac_status
from .presentation import present
from .privacy import privacy_report
from .reports import build_report
from .wifi_audit import wifi_audit
from .zeek import summarize_zeek


def main() -> int:
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        print("GhostPath GUI must not run as root.", file=sys.stderr)
        return 2
    try:
        from PySide6.QtCore import QObject, Qt, QRunnable, QThreadPool, Signal
        from PySide6.QtWidgets import (
            QApplication, QComboBox, QFileDialog, QFrame, QGridLayout,
            QHBoxLayout, QLabel, QMainWindow, QMessageBox, QPlainTextEdit,
            QPushButton, QScrollArea, QTabWidget, QVBoxLayout, QWidget,
        )
    except ImportError:
        print("Install optional PySide6 GUI with: bash scripts/install-user.sh --gui", file=sys.stderr)
        return 2

    def label(text: object, style: str = "") -> QLabel:
        widget = QLabel(str(text))
        widget.setTextFormat(Qt.PlainText)
        widget.setWordWrap(True)
        widget.setTextInteractionFlags(Qt.TextSelectableByMouse)
        if style:
            widget.setObjectName(style)
        return widget

    class TaskSignals(QObject):
        finished = Signal(object)
        failed = Signal(str)

    class Task(QRunnable):
        def __init__(self, fn):
            super().__init__()
            self.fn = fn
            self.signals = TaskSignals()

        def run(self):
            try:
                self.signals.finished.emit(self.fn())
            except Exception as exc:
                self.signals.failed.emit(type(exc).__name__ + ": " + str(exc))

    class View(QWidget):
        def __init__(self, title: str, description: str):
            super().__init__()
            self.title = title
            self.description = description
            self.current: dict[str, object] | None = None
            self.root = QVBoxLayout(self)
            self.root.setContentsMargins(20, 16, 20, 14)
            self.root.setSpacing(12)
            self.heading = label(title, "sectionTitle")
            self.root.addWidget(self.heading)
            self.subtitle = label(description, "subcopy")
            self.root.addWidget(self.subtitle)

            self.actions = QHBoxLayout()
            self.actions.setSpacing(8)
            self.root.addLayout(self.actions)

            self.provenance = label("Read-only / offline", "provenance")
            self.root.addWidget(self.provenance)

            self.scroll = QScrollArea()
            self.scroll.setWidgetResizable(True)
            self.scroll.setFrameShape(QFrame.NoFrame)
            self.content = QWidget()
            self.body = QVBoxLayout(self.content)
            self.body.setContentsMargins(0, 0, 2, 4)
            self.body.setSpacing(12)
            self.summary = label("Select Refresh to load local diagnostics.", "summary")
            self.body.addWidget(self.summary)
            self.metrics = QGridLayout()
            self.metrics.setSpacing(10)
            self.body.addLayout(self.metrics)
            self.finding_header = label("Findings and next steps", "subheading")
            self.body.addWidget(self.finding_header)
            self.finding_list = QVBoxLayout()
            self.finding_list.setSpacing(8)
            self.body.addLayout(self.finding_list)
            self.caution = label(
                "Evidence limits and privacy warnings will appear here.",
                "caution",
            )
            self.body.addWidget(self.caution)
            self.body.addStretch(1)
            self.scroll.setWidget(self.content)
            self.root.addWidget(self.scroll, 1)

            self.details_btn = QPushButton("Show technical details")
            self.details_btn.setObjectName("detailsToggle")
            self.details_btn.setCheckable(True)
            self.details_btn.setChecked(False)
            self.details_btn.toggled.connect(self.toggle_details)
            self.root.addWidget(self.details_btn)
            self.raw = QPlainTextEdit()
            self.raw.setReadOnly(True)
            self.raw.setVisible(False)
            self.raw.setObjectName("technicalDetails")
            self.raw.setAccessibleName(f"{title} technical JSON details")
            self.raw.setPlaceholderText("Technical JSON appears after Refresh.")
            self.root.addWidget(self.raw, 1)

        def add_action(self, widget: QWidget) -> None:
            self.actions.addWidget(widget)

        def toggle_details(self, checked: bool) -> None:
            self.raw.setVisible(checked)
            self.scroll.setVisible(not checked)
            self.details_btn.setText(
                "Hide technical details" if checked else "Show technical details"
            )

        def _clear(self, layout) -> None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                child_layout = item.layout()
                if child_layout is not None:
                    self._clear(child_layout)

        def show_loading(self) -> None:
            self.summary.setText("Reading permitted local or offline information…")

        def show_error(self, message: str) -> None:
            self.summary.setText("This assessment could not be completed.")
            self.caution.setText(message)
            self.provenance.setText("No new finding verified")
            self._clear(self.metrics)
            self._clear(self.finding_list)
            self.finding_header.setVisible(False)
            self.raw.setPlainText("Error: " + message)

        def display(self, data: dict[str, object]) -> None:
            view = present(self.title, data)
            self.current = data
            self.heading.setText(view["title"])
            self.provenance.setText("EVIDENCE SOURCE  •  " + view["provenance"])
            self.summary.setText(view["summary"])
            self.caution.setText(view["caution"])
            self._clear(self.metrics)
            for i, card in enumerate(view["cards"]):
                tile = QFrame()
                tile.setObjectName("metricCard")
                tile.setAccessibleName(
                    str(card["label"]) + ": " + str(card["value"])
                )
                layout = QVBoxLayout(tile)
                layout.setContentsMargins(14, 12, 14, 12)
                layout.setSpacing(5)
                layout.addWidget(label(card["label"], "metricLabel"))
                value = label(card["value"], "metricValue")
                if card.get("status") == "warning":
                    value.setProperty("risk", "warning")
                elif card.get("status") == "good":
                    value.setProperty("risk", "good")
                layout.addWidget(value)
                self.metrics.addWidget(tile, i // 3, i % 3)

            self._clear(self.finding_list)
            self.finding_header.setVisible(bool(view["findings"]))
            for finding in view["findings"]:
                item = QFrame()
                item.setObjectName("findingCard")
                sublayout = QVBoxLayout(item)
                sublayout.setContentsMargins(12, 9, 12, 9)
                sublayout.setSpacing(4)
                badge_text = str(finding["severity"]).upper()
                sublayout.addWidget(label(badge_text + "  •  " + finding["title"], "findingTitle"))
                if finding["detail"]:
                    sublayout.addWidget(label(finding["detail"], "findingDetail"))
                self.finding_list.addWidget(item)
            self.raw.setPlainText(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))

    class Window(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("GhostPath v2 — Defensive Security")
            self.resize(1120, 760)
            self.setMinimumSize(820, 570)
            self.jobs = []
            self.pending: dict[str, int] = {}
            self.offline_import: dict[str, object] | None = None
            self.pool = QThreadPool.globalInstance()
            shell = QWidget()
            shell_layout = QVBoxLayout(shell)
            shell_layout.setContentsMargins(12, 12, 12, 6)
            shell_layout.setSpacing(10)
            brand = QHBoxLayout()
            name = label("GHOSTPATH  /  SECURITY WORKSPACE", "brand")
            brand.addWidget(name)
            brand.addStretch()
            chip = label("DEVELOPMENT ALPHA · READ-ONLY", "statusChip")
            brand.addWidget(chip)
            shell_layout.addLayout(brand)
            self.tabs = QTabWidget()
            self.tabs.setDocumentMode(True)
            self.tabs.setMovable(False)
            self.tabs.setUsesScrollButtons(True)
            shell_layout.addWidget(self.tabs, 1)
            self.setCentralWidget(shell)
            self.pages: dict[str, View] = {}

            definitions = [
                ("Dashboard", "Local system health and dependency status.", doctor),
                ("Privacy", "Tor, local SOCKS and DNS diagnostic results.", privacy_report),
                ("MAC Privacy", "Network interface summary and privacy profile previews.", mac_status),
                ("Wi-Fi Audit", "Security posture from cached, connected network details.", wifi_audit),
                ("DDoS Defence", "Offline synthetic traffic analysis and interpretation.",
                 lambda: analyze(example_events("surge"))),
                ("Learning Labs", "Guided offline training scenarios.", list_labs),
                ("Router JSON", "Check an authorised local router configuration file.",
                 lambda: {"hint": "Choose Open Local File to assess a router JSON export."}),
                ("Suricata EVE", "Review authorised previously collected alert logs.",
                 lambda: {"hint": "Choose Open Local File to import a Suricata log."}),
                ("Zeek JSON", "Summarise authorised previously collected connection logs.",
                 lambda: {"hint": "Choose Open Local File to import Zeek JSON."}),
                ("Learning", "Self-guided lessons, no network traffic.", list_lessons),
                ("Reports", "Export an easy-to-read local HTML assessment.",
                 lambda: {"hint": "Choose Export HTML to create a private report."}),
            ]
            self.actions = {title: fn for title, _, fn in definitions}

            for title, description, fn in definitions:
                panel = View(title, description)
                refresh = QPushButton("Refresh")
                refresh.setAccessibleName(f"Refresh {title}")
                refresh.clicked.connect(
                    lambda _, t=title, f=fn: self.run_task(t, f)
                )
                panel.add_action(refresh)

                if title == "MAC Privacy":
                    profiles = QComboBox()
                    profiles.addItems(["preserve", "stable", "random"])
                    profiles.setAccessibleName("Select MAC privacy profile preview")
                    panel.add_action(profiles)
                    preview = QPushButton("Preview profile")
                    preview.clicked.connect(
                        lambda _, t=title, box=profiles:
                        self.run_task(t, lambda: plan(box.currentText()))
                    )
                    panel.add_action(preview)
                if title in ("Router JSON", "Suricata EVE", "Zeek JSON"):
                    select = QPushButton("Open local file")
                    select.clicked.connect(lambda _, t=title: self.select_file(t))
                    panel.add_action(select)
                if title == "Reports":
                    export = QPushButton("Export HTML report")
                    export.setObjectName("reportExport")
                    export.clicked.connect(self.export_html)
                    panel.add_action(export)
                if title == "Learning":
                    picker = QComboBox()
                    picker.addItems(["tor", "mac", "wifi", "ddos", "report"])
                    panel.add_action(picker)
                    read = QPushButton("Read lesson")
                    read.clicked.connect(
                        lambda _, t=title, box=picker:
                        self.run_task(t, lambda: read_lesson(box.currentText()))
                    )
                    panel.add_action(read)
                if title == "Learning Labs":
                    picker = QComboBox()
                    picker.addItems([
                        "traffic-baseline", "traffic-anomaly", "wifi-hardening", "mac-privacy",
                    ])
                    panel.add_action(picker)
                    run = QPushButton("Run offline lab")
                    run.clicked.connect(
                        lambda _, t=title, box=picker:
                        self.run_task(t, lambda: run_lab(box.currentText()))
                    )
                    panel.add_action(run)
                self.pages[title] = panel
                self.tabs.addTab(panel, title)
            self.tabs.currentChanged.connect(self.on_tab_change)
            self.statusBar().showMessage(
                "Read-only diagnostics and offline education. No privacy protection is active or verified."
            )
            self.run_task("Dashboard", doctor)

        def on_tab_change(self, index: int) -> None:
            title = self.tabs.tabText(index)
            if title in self.pages and self.pages[title].current is None:
                self.run_task(title, self.actions[title])

        def select_file(self, title: str) -> None:
            if title == "Router JSON":
                file_filter = "JSON files (*.json)"
                callback = audit_router_file
            elif title == "Suricata EVE":
                file_filter = "EVE logs (*.json *.jsonl)"
                callback = summarize_eve
            elif title == "Zeek JSON":
                file_filter = "Zeek JSON logs (*.json *.jsonl *.log)"
                callback = summarize_zeek
            else:
                return
            path, _ = QFileDialog.getOpenFileName(
                self, f"Open authorised {title} file", str(Path.home()), file_filter,
            )
            if path:
                self.run_task(title, lambda: callback(Path(path)), imported=True)

        def export_html(self) -> None:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Create private HTML assessment", "ghostpath-report.html",
                "HTML reports (*.html)",
            )
            if not filename:
                return
            def generate():
                data = build_report()
                if self.offline_import is not None:
                    data["offline_imported_evidence"] = self.offline_import
                return save_html_report(data, Path(filename))
            self.run_task("Reports", generate)

        def run_task(self, title: str, callback, imported: bool = False) -> None:
            panel = self.pages[title]
            panel.show_loading()
            self.pending[title] = self.pending.get(title, 0) + 1
            generation = self.pending[title]
            task = Task(callback)
            self.jobs.append(task)

            def on_finished(payload):
                if generation == self.pending[title]:
                    if isinstance(payload, dict):
                        panel.display(payload)
                        if imported:
                            # Importers return only limited, redacted metadata.
                            self.offline_import = {
                                "source": title,
                                "provenance": "Offline imported evidence",
                                "results": payload,
                            }
                    else:
                        panel.show_error("Unsupported response from this module.")
                if task in self.jobs:
                    self.jobs.remove(task)

            def on_failed(message):
                if generation == self.pending[title]:
                    panel.show_error(message)
                if task in self.jobs:
                    self.jobs.remove(task)

            task.signals.finished.connect(on_finished)
            task.signals.failed.connect(on_failed)
            self.pool.start(task)

    app = QApplication.instance() or QApplication(sys.argv[:1])
    app.setApplicationName("GhostPath")
    app.setStyleSheet("""
        QWidget { background: #111a27; color: #e9f1fc; font-size: 13px; }
        QMainWindow { background: #0b1320; }
        QLabel#brand { font-weight: 800; font-size: 15px; color: #80c7ef; }
        QLabel#statusChip {
            color: #edc98d; background: #303023; border: 1px solid #59533a;
            padding: 6px 10px; border-radius: 9px; font-weight: 700; font-size: 11px;
        }
        QTabWidget::pane { border: 1px solid #334359; border-radius: 8px; }
        QTabBar::tab {
            background: #1b293b; color: #cedbea; padding: 10px 15px;
            margin-right: 3px; border-radius: 5px;
        }
        QTabBar::tab:selected { background: #255c86; color: white; }
        QTabBar::tab:hover { background: #304665; }
        QLabel#sectionTitle { font-size: 22px; font-weight: 800; color: #f4f8ff; }
        QLabel#subcopy { color: #a5b7cf; font-size: 13px; }
        QLabel#provenance {
            color: #7dccdd; font-weight: 700; font-size: 11px;
            background: #19303e; padding: 7px 10px; border-radius: 7px;
        }
        QLabel#summary { font-size: 14px; color: #d8e6f4; }
        QLabel#subheading { font-size: 15px; font-weight: 700; }
        QLabel#metricLabel { color: #a6bad0; font-size: 11px; }
        QLabel#metricValue { font-size: 19px; font-weight: 800; color: #f0f6ff; }
        QLabel#metricValue[risk="warning"] { color: #f1c57e; }
        QLabel#metricValue[risk="good"] { color: #8bdfc5; }
        QLabel#findingTitle { font-weight: 700; color: #f2e3c0; }
        QLabel#findingDetail { color: #c4d3e3; }
        QLabel#caution {
            color: #e2c58f; background: #292824;
            border: 1px solid #63553a; border-radius: 8px;
            padding: 12px;
        }
        QFrame#metricCard {
            border: 1px solid #354961; border-radius: 10px;
            background: #1b2a3d; min-height: 65px;
        }
        QFrame#findingCard {
            border: 1px solid #394a61; border-radius: 8px; background: #1c2a3a;
        }
        QPushButton {
            color: #eef7ff; background: #255c86; border: 1px solid #477ca5;
            padding: 9px 15px; border-radius: 7px; font-weight: 700;
        }
        QPushButton:hover { background: #327caa; }
        QPushButton:focus { border: 2px solid #8acefb; }
        QPushButton#detailsToggle { background: #202f44; }
        QPushButton#reportExport { background: #207867; }
        QComboBox {
            color: #e9f1fc; background: #23354b;
            border: 1px solid #47617e; padding: 7px; border-radius: 7px;
        }
        QPlainTextEdit {
            background: #132235; color: #d1e3f1; border: 1px solid #3a526d;
            border-radius: 8px; padding: 9px; font-family: monospace;
        }
        QScrollArea { border: none; }
        QStatusBar { background: #0d1825; color: #efc68a; }
    """)
    window = Window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
