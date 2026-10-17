"""Optional PySide6 diagnostic desktop interface.

No root privileges, Wi-Fi scans, firewall/DNS modifications or active traffic.
"""
from __future__ import annotations

import json
import os
import sys

from .defense import analyze, example_events
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
            QPlainTextEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget,
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
                        self.run_task(view_title, lambda selected=c.currentText(): plan(selected))
                    )
                if title == "Learning Labs":
                    selector = QComboBox()
                    selector.addItems(["traffic-baseline", "traffic-anomaly", "wifi-hardening", "mac-privacy"])
                    launch = QPushButton("Run Offline Lab")
                    buttons.addWidget(selector)
                    buttons.addWidget(launch)
                    launch.clicked.connect(
                        lambda _, view_title=title, c=selector:
                        self.run_task(view_title, lambda selected=c.currentText(): run_lab(selected))
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
