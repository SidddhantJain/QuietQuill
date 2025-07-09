# ui/mood_tracker.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QInputDialog, QMessageBox
import os, json
from PyQt5.QtCore import QDate

class MoodTrackerWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("📅 Mood Tracker")
        self.setGeometry(400, 200, 400, 400)
        self.mood_file = os.path.join("entries", self.username, "moods.json")
        self.mood_data = self.load_mood_data()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.set_mood_for_day)
        layout.addWidget(self.calendar)

        self.setLayout(layout)
        self.update_calendar_marks()

    def load_mood_data(self):
        if os.path.exists(self.mood_file):
            with open(self.mood_file, "r") as f:
                return json.load(f)
        return {}

    def set_mood_for_day(self, date: QDate):
        selected_date = date.toString("yyyy-MM-dd")
        mood, ok = QInputDialog.getText(self, "Select Mood", "Enter emoji for mood (e.g., 😊, 😔, 😎, 😡, 🥳):")
        if ok and mood.strip():
            self.mood_data[selected_date] = mood.strip()
            with open(self.mood_file, "w") as f:
                json.dump(self.mood_data, f, indent=2)
            QMessageBox.information(self, "Mood Saved", f"Mood for {selected_date}: {mood}")
            self.update_calendar_marks()

    def update_calendar_marks(self):
        fmt = self.calendar.dateTextFormat(QDate.currentDate())
        fmt.setFontWeight(0)

        for date_str, emoji in self.mood_data.items():
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            fmt = self.calendar.dateTextFormat(date)
            fmt.setToolTip(emoji)
            self.calendar.setDateTextFormat(date, fmt)
