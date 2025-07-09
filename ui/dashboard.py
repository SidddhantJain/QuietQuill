import os
import json
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget,
    QMessageBox, QHBoxLayout, QLineEdit, QDesktopWidget
)
from PyQt5.QtCore import Qt
from ui.editor import EditorWindow
from PyQt5.QtWidgets import QCheckBox, QApplication


class DashboardWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.theme = "light"  # default
        self.setWindowTitle(f"QuietQuill - Dashboard ({self.username})")

        # Set window size to 80% of the screen
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.8)
        height = int(screen.height() * 0.8)
        self.setGeometry(
            (screen.width() - width) // 2,
            (screen.height() - height) // 2,
            width,
            height
        )

        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        # Welcome title
        title = QLabel(f"📔 Welcome, <b>{self.username}</b>")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px;")
        self.layout.addWidget(title)

        # 🌙 Theme Toggle
        theme_toggle_row = QHBoxLayout()
        self.theme_toggle = QCheckBox("🌙 Dark Mode")
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        theme_toggle_row.addStretch()
        theme_toggle_row.addWidget(self.theme_toggle)
        self.layout.addLayout(theme_toggle_row)

        # 🔍 Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search by tag, title or date...")
        self.search_bar.textChanged.connect(self.filter_entries)
        self.layout.addWidget(self.search_bar)

        # 📄 Entry list
        self.entry_list = QListWidget()
        self.layout.addWidget(self.entry_list)

        # 🔘 Action buttons
        button_row = QHBoxLayout()

        
        open_btn = QPushButton("🔓 Open Entry")
        open_btn.clicked.connect(self.open_entry)

        
        new_btn = QPushButton("➕ New Entry")
        new_btn.clicked.connect(self.new_entry)

        
        delete_btn = QPushButton("🗑️ Delete Entry")
        delete_btn.clicked.connect(self.delete_entry)

        
        change_pw_btn = QPushButton("🔐 Change Password")
        change_pw_btn.clicked.connect(self.change_password)

        
        mood_btn = QPushButton("📅 Mood Tracker")
        mood_btn.clicked.connect(self.open_mood_tracker)
        button_row.addWidget(mood_btn)

        
        # Calander button
        calendar_btn = QPushButton("📆 View Calendar")
        calendar_btn.clicked.connect(self.open_entry_calendar)
        button_row.addWidget(calendar_btn)

        # Entry stats button
        stats_btn = QPushButton("📈 Entry Stats")
        stats_btn.clicked.connect(self.open_stats)
        button_row.addWidget(stats_btn)

        # Advanced search button
        self.advanced_search_btn = QPushButton("🔍 Advanced Search")
        self.advanced_search_btn.clicked.connect(self.open_advanced_search)
        self.layout.addWidget(self.advanced_search_btn)


        # Logout button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.clicked.connect(self.logout)

        button_row.addWidget(open_btn)
        button_row.addWidget(new_btn)
        button_row.addWidget(delete_btn)
        button_row.addWidget(change_pw_btn)
        button_row.addWidget(logout_btn)

        self.layout.addLayout(button_row)
        self.setLayout(self.layout)

        # Load entries at the end
        self.load_entries()
    
    def toggle_theme(self):
        current = self.styleSheet()
        if "background: qlineargradient" in current:
            # Switch to light theme
            self.setStyleSheet("""
                QWidget {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #f0f9ff, stop: 0.5 #cfe8ff, stop: 1 #a6d1ff
                    );
                    color: #000000;
                    font-family: Arial, sans-serif;
                }
                QPushButton {
                    background-color: #e6f7ff;
                    border: 1px solid #80bfff;
                    border-radius: 8px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #cceeff;
                }
                QLineEdit {
                    background-color: #ffffff;
                    border: 1px solid #80bfff;
                    border-radius: 8px;
                    padding: 8px;
                }
                QListWidget {
                    background-color: #ffffff;
                    border: 1px solid #80bfff;
                    border-radius: 8px;
                }
                QLabel {
                    font-size: 20px;
                    font-weight: bold;
                    color: #004080;
                }
            """)
        else:
            # Switch to dark theme
            self.setStyleSheet("""
                QWidget {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #1a1a2e, stop: 0.5 #16213e, stop: 1 #0f3460
                    );
                    color: #f0f0f0;
                    font-family: Arial, sans-serif;
                }
                QPushButton {
                    background-color: #1f4068;
                    border: 1px solid #16213e;
                    border-radius: 8px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1b3a57;
                }
                QLineEdit {
                    background-color: #16213e;
                    border: 1px solid #1f4068;
                    border-radius: 8px;
                    padding: 8px;
                }
                QListWidget {
                    background-color: #16213e;
                    border: 1px solid #1f4068;
                    border-radius: 8px;
                }
                QLabel {
                    font-size: 20px;
                    font-weight: bold;
                    color: #e6e6e6;
                }
            """)


    def open_stats(self):
        from ui.stats import StatsWindow
        self.stats_window = StatsWindow(self.username)
        self.stats_window.show()


    def get_entry_dir(self):
        return os.path.join("entries", self.username)
    
    def open_entry_calendar(self):
        from ui.entry_calendar import EntryCalendarWindow
        self.calendar_window = EntryCalendarWindow(self.username)
        self.calendar_window.show()

    
    def open_mood_tracker(self):
        from ui.mood_tracker import MoodTrackerWindow
        self.mood_window = MoodTrackerWindow(self.username)
        self.mood_window.show()


    def open_advanced_search(self):
        from ui.advanced_search import AdvancedSearchWindow
        self.search_window = AdvancedSearchWindow(self.username)
        self.search_window.show()


    def load_entries(self):
        self.entry_list.clear()
        self.all_entries = []

        entry_path = self.get_entry_dir()
        for root, _, files in os.walk(entry_path):
            for file in files:
                if file.endswith(".enc"):
                    meta_file = file.replace(".enc", ".meta.json")
                    meta_path = os.path.join(root, meta_file)
                    if os.path.exists(meta_path):
                        with open(meta_path, "r") as f:
                            meta = json.load(f)
                            label = f"{meta.get('title')} | {meta.get('start_time')} → {meta.get('end_time', '---')}"
                            tags = meta.get("tags", [])
                            if tags:
                                label += f"\nTags: {', '.join(tags)}"
                            self.all_entries.append((label, file))
                    else:
                        self.all_entries.append((file, file))  # fallback
        self.refresh_entry_list()
    def new_entry(self):
        self.editor = EditorWindow(self.username, theme=self.theme)
        self.editor.show()

    def open_entry(self):
        selected = self.entry_list.currentItem()
        if selected:
            filename = selected.data(Qt.UserRole)
            self.editor = EditorWindow(self.username, filename=filename, theme=self.theme)
            self.editor.show()


    def refresh_entry_list(self):
        self.entry_list.clear()
        for label, _ in self.all_entries:
            self.entry_list.addItem(label)

    def filter_entries(self, text):
        text = text.lower()
        filtered = [(label, fname) for label, fname in self.all_entries if text in label.lower()]
        self.entry_list.clear()
        for label, _ in filtered:
            self.entry_list.addItem(label)

    def find_file_path(self, filename):
        entry_dir = self.get_entry_dir()
        for root, _, files in os.walk(entry_dir):
            if filename in files:
                return os.path.join(root, filename)
        return None

    def open_entry(self):
        index = self.entry_list.currentRow()
        if index >= 0:
            _, file = self.all_entries[index]
            self.editor = EditorWindow(self.username, file)
            self.editor.show()
        else:
            QMessageBox.warning(self, "No Selection", "Please select an entry.")

    def new_entry(self):
        self.editor = EditorWindow(self.username)
        self.editor.show()

    def delete_entry(self):
        index = self.entry_list.currentRow()
        if index >= 0:
            label, file = self.all_entries[index]
            confirm = QMessageBox.question(self, "Confirm Delete", f"Delete entry:\n\n{label}?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                path = self.find_file_path(file)
                if path:
                    os.remove(path)
                    meta_path = path.replace(".enc", ".meta.json")
                    if os.path.exists(meta_path):
                        os.remove(meta_path)
                    self.load_entries()
                else:
                    QMessageBox.warning(self, "Error", "Could not find the selected entry.")
        else:
            QMessageBox.warning(self, "No Selection", "Select an entry to delete.")

    def change_password(self):
        from ui.change_password import ChangePasswordWindow
        self.change_window = ChangePasswordWindow(self.username)
        self.change_window.show()

    def logout(self):
        from ui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()