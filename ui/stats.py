from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
import os, json

class StatsWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("📊 Entry Statistics")
        self.setGeometry(550, 250, 350, 250)
        self.entry_dir = os.path.join("entries", username)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        total_entries = 0
        longest_entry = 0
        wordiest_title = ""
        date_count = {}

        for file in os.listdir(self.entry_dir):
            if file.endswith(".meta.json"):
                total_entries += 1
                meta_path = os.path.join(self.entry_dir, file)
                with open(meta_path) as f:
                    meta = json.load(f)
                word_count = meta.get("word_count", 0)
                if word_count > longest_entry:
                    longest_entry = word_count
                    wordiest_title = meta.get("title", "")
                date = meta.get("date", "")
                date_count[date] = date_count.get(date, 0) + 1

        most_active_day = max(date_count.items(), key=lambda x: x[1], default=("N/A", 0))

        layout.addWidget(QLabel(f"📝 Total Entries: {total_entries}"))
        layout.addWidget(QLabel(f"📚 Longest Entry: {wordiest_title} ({longest_entry} words)"))
        layout.addWidget(QLabel(f"📆 Most Active Day: {most_active_day[0]} ({most_active_day[1]} entries)"))
        self.setLayout(layout)
