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
        total_words = 0
        dates = []

        if not os.path.isdir(self.entry_dir):
            layout.addWidget(QLabel("No entries found for this user."))
            self.setLayout(layout)
            return

        for file in os.listdir(self.entry_dir):
            if file.endswith(".meta.json"):
                try:
                    total_entries += 1
                    meta_path = os.path.join(self.entry_dir, file)
                    with open(meta_path) as f:
                        meta = json.load(f)
                    word_count = meta.get("word_count", 0)
                    total_words += word_count
                    if word_count > longest_entry:
                        longest_entry = word_count
                        wordiest_title = meta.get("title", "")
                    date = meta.get("date", "")
                    if date:
                        date_count[date] = date_count.get(date, 0) + 1
                        dates.append(date)
                except Exception:
                    continue

        most_active_day = max(date_count.items(), key=lambda x: x[1], default=("N/A", 0))
        avg_words = total_words // total_entries if total_entries else 0
        earliest = min(dates) if dates else "N/A"
        latest = max(dates) if dates else "N/A"

        layout.addWidget(QLabel(f"📝 Total Entries: {total_entries}"))
        layout.addWidget(QLabel(f"📚 Longest Entry: {wordiest_title} ({longest_entry} words)"))
        layout.addWidget(QLabel(f"✍️ Average Words per Entry: {avg_words}"))
        layout.addWidget(QLabel(f"📆 Most Active Day: {most_active_day[0]} ({most_active_day[1]} entries)"))
        layout.addWidget(QLabel(f"⏳ Earliest Entry: {earliest}"))
        layout.addWidget(QLabel(f"🕰️ Latest Entry: {latest}"))
        self.setLayout(layout)
