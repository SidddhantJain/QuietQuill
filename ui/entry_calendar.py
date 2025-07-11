from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QMessageBox, QListWidget, QDialog, QDialogButtonBox
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QColor
import os, json

class EntryCalendarWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("📆 Entry Calendar")
        self.setGeometry(500, 200, 400, 400)
        self.entry_dir = os.path.join("entries", username)
        self.setup_ui()
        self.mark_entry_dates()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.show_entry_info)
        layout.addWidget(self.calendar)
        self.setLayout(layout)

    def mark_entry_dates(self):
        # Highlight dates with entries
        if not os.path.isdir(self.entry_dir):
            return
        dates_with_entries = set()
        for file in os.listdir(self.entry_dir):
            if file.endswith(".meta.json"):
                try:
                    with open(os.path.join(self.entry_dir, file)) as f:
                        meta = json.load(f)
                        date_str = meta.get("date")
                        if date_str:
                            dates_with_entries.add(date_str)
                except Exception:
                    continue
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#cce5ff"))
        for date_str in dates_with_entries:
            try:
                qdate = QDate.fromString(date_str, "yyyy-MM-dd")
                if qdate.isValid():
                    self.calendar.setDateTextFormat(qdate, fmt)
            except Exception:
                continue

    def show_entry_info(self, date: QDate):
        date_str = date.toString("yyyy-MM-dd")
        entries = []
        if not os.path.isdir(self.entry_dir):
            QMessageBox.information(self, "No Entries", "No entries directory found for this user.")
            return
        for file in os.listdir(self.entry_dir):
            if file.endswith(".meta.json"):
                try:
                    with open(os.path.join(self.entry_dir, file)) as f:
                        meta = json.load(f)
                        if meta.get("date") == date_str:
                            entries.append(meta.get("title", file))
                except Exception:
                    continue
        if entries:
            if len(entries) == 1:
                QMessageBox.information(self, "Entry", entries[0])
            else:
                self.show_entries_list(entries)
        else:
            QMessageBox.information(self, "No Entries", "No entries for this day.")

    def show_entries_list(self, entries):
        dialog = QDialog(self)
        dialog.setWindowTitle("Entries")
        layout = QVBoxLayout(dialog)
        list_widget = QListWidget()
        list_widget.addItems(entries)
        layout.addWidget(list_widget)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)
        dialog.exec_()
