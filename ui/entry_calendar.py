from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QMessageBox
from PyQt5.QtCore import QDate
import os, json

class EntryCalendarWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("📆 Entry Calendar")
        self.setGeometry(500, 200, 400, 400)
        self.entry_dir = os.path.join("entries", username)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.show_entry_info)
        layout.addWidget(self.calendar)
        self.setLayout(layout)

    def show_entry_info(self, date: QDate):
        date_str = date.toString("yyyy-MM-dd")
        entries = []
        for file in os.listdir(self.entry_dir):
            if file.endswith(".meta.json"):
                with open(os.path.join(self.entry_dir, file)) as f:
                    meta = json.load(f)
                    if meta.get("date") == date_str:
                        entries.append(meta.get("title", file))
        if entries:
            QMessageBox.information(self, "Entries", "\n".join(entries))
        else:
            QMessageBox.information(self, "No Entries", "No entries for this day.")
