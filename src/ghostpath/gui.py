"""Optional PySide6 diagnostic desktop interface.

No root privileges, Wi-Fi scans, firewall/DNS modifications or active traffic.
"""
from __future__ import annotations

import json
import os
import sys

from .defense import analyze, example_events
from .config_audit import audit_file as audit_router_file
from .eve import summarize_eve
from .html_reports import save_html_report
from .lessons import list_lessons, read_lesson
from .reports import build_report
from .diagnostics import doctor
from .labs import list_labs, run_lab
from .mac_privacy import plan, status as mac_status
from .privacy import privacy_report
from .wifi_audit import wifi_audit


def main() -> int:
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        print("GhostPath GUI must not run as root.", file=sys.stderr)
        return 2
    try:
        from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal
        from PySide6.QtWidgets import (
            QApplication, QComboBox, QHBoxLayout, QLabel, QMainWindow,
            QMessageBox, QPlainTextEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget, QFileDialog,
        )
    except ImportError:
        print("Desktop UI requires optional PySide6: python -m pip install 'ghostpath[gui]'", file=sys.stderr)
        return 2

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

    class Window(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("GhostPath v2 — Privacy & Defence Learning")
            self.resize(920, 650)
            self.workers = []
            self.pool = QThreadPool.globalInstance()
            tabs = QTabWidget()
            self.setCentralWidget(tabs)
            self.views = {}

            definitions = [
                ("Dashboard", "Local health diagnostics", doctor),
                ("Privacy", "Tor SOCKS and DNS diagnostics", privacy_report),
                ("MAC Privacy", "Current interfaces and planned profiles", mac_status),
                ("Wi-Fi Audit", "Connected-network configuration review", wifi_audit),
                ("DDoS Defence", "Synthetic data analytics only", lambda: analyze(example_events("surge"))),
                ("Learning Labs", "Offline exercises", list_labs),
                ("Router JSON", "Authorised router settings from a local file only", lambda: {"hint": "Open a local JSON configuration file"}),
                ("Suricata EVE", "Offline defensive IDS alert logs only", lambda: {"hint": "Open a local EVE JSONL file"}),
                ("Learning", "Offline educational lessons", list_lessons),
                ("Reports", "Export an escaped, private HTML report", lambda: {"hint": "Click Export HTML"}),
            ]
            for title, description, fn in definitions:
                panel = QWidget()
                layout = QVBoxLayout(panel)
                label = QLabel(description + "\nNo automatic network changes or external tests.")
                layout.addWidget(label)
                buttons = QHBoxLayout()
                refresh = QPushButton("Refresh")
                buttons.addWidget(refresh)
                if title == "MAC Privacy":
                    selector = QComboBox()
                    selector.addItems(["preserve", "stable", "random"])
                    preview = QPushButton("Preview Profile")
                    buttons.addWidget(selector)
                    buttons.addWidget(preview)
                    preview.clicked.connect(
                        lambda _, view_title=title, c=selector:
                        self.run_task(view_title, lambda: plan(c.currentText()))
                    )
                if title in ("Router JSON", "Suricata EVE"):
                    open_file = QPushButton("Open Local File")
                    buttons.addWidget(open_file)
                    open_file.clicked.connect(lambda _, view_title=title: self.select_file(view_title))
                if title == "Reports":
                    save = QPushButton("Export HTML")
                    buttons.addWidget(save)
                    save.clicked.connect(lambda _: self.export_html())
                if title == "Learning":
                    selector = QComboBox()
                    selector.addItems(["tor", "mac", "wifi", "ddos", "report"])
                    show = QPushButton("Read Lesson")
                    buttons.addWidget(selector)
                    buttons.addWidget(show)
                    show.clicked.connect(lambda _, view_title=title, c=selector:
                        self.run_task(view_title, lambda: read_lesson(c.currentText())))
                if title == "Learning Labs":
                    selector = QComboBox()
                    selector.addItems(["traffic-baseline", "traffic-anomaly", "wifi-hardening", "mac-privacy"])
                    launch = QPushButton("Run Offline Lab")
                    buttons.addWidget(selector)
                    buttons.addWidget(launch)
                    launch.clicked.connect(
                        lambda _, view_title=title, c=selector:
                        self.run_task(view_title, lambda: run_lab(c.currentText()))
                    )
                layout.addLayout(buttons)
                view = QPlainTextEdit()
                view.setReadOnly(True)
                view.setPlaceholderText("Click Refresh for local, read-only diagnostics.")
                layout.addWidget(view)
                self.views[title] = view
                refresh.clicked.connect(
                    lambda _, view_title=title, function=fn:
                    self.run_task(view_title, function)
                )
                tabs.addTab(panel, title)
            tabs.currentChanged.connect(self.on_tab_change)
            self.definitions = {title: fn for title, _, fn in definitions}
            self.statusBar().showMessage("No privacy protection is active or verified.")

        def on_tab_change(self, index: int):
            title = self.centralWidget().tabText(index)
            if not self.views[title].toPlainText():
                self.run_task(title, self.definitions[title])

        def select_file(self, title):
            if title == "Router JSON":
                name, _ = QFileDialog.getOpenFileName(self, "Router configuration", "", "JSON files (*.json)")
                if name:
                    self.run_task(title, lambda: audit_router_file(__import__("pathlib").Path(name)))
            elif title == "Suricata EVE":
                name, _ = QFileDialog.getOpenFileName(self, "Offline Suricata EVE", "", "JSONL (*.jsonl *.json)")
                if name:
                    self.run_task(title, lambda: summarize_eve(__import__("pathlib").Path(name)))

        def export_html(self):
            name, _ = QFileDialog.getSaveFileName(self, "Private HTML report", "ghostpath-report.html", "HTML (*.html)")
            if name:
                self.run_task("Reports", lambda: save_html_report(build_report(), __import__("pathlib").Path(name)))

        def run_task(self, title, callback):
            view = self.views[title]
            view.setPlainText("Reading local diagnostics...")
            job = Task(callback)
            self.workers.append(job)
            def finished(payload):
                view.setPlainText(json.dumps(payload, indent=2, sort_keys=True))
                if job in self.workers:
                    self.workers.remove(job)
            def failed(message):
                view.setPlainText("Unable to complete diagnostic: " + message)
                if job in self.workers:
                    self.workers.remove(job)
            job.signals.finished.connect(finished)
            job.signals.failed.connect(failed)
            self.pool.start(job)

    app = QApplication.instance() or QApplication(sys.argv[:1])
    window = Window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
