import os
import json
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget,
    QMessageBox, QHBoxLayout, QLineEdit, QDesktopWidget,
    QCheckBox, QSpacerItem, QSizePolicy, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from ui.editor import EditorWindow


class DashboardWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.theme = "light"  # default
        self.setWindowTitle(f"QuietQuill - Dashboard ({self.username})")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background-color: #e3f2fd;")
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Title above the card
        self.title = QLabel(f"📔 <b>Welcome, {self.username}</b>")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("dashboardTitle")
        self.main_layout.addWidget(self.title, alignment=Qt.AlignHCenter)
        self.main_layout.addSpacing(8)

        # Card frame with gradient and shadow
        self.card_frame = QFrame()
        self.card_frame.setObjectName("dashboardCard")
        self.card_frame.setStyleSheet("""
            QFrame#dashboardCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff, stop:1 #e3f2fd);
                border-radius: 22px;
                padding: 36px 36px 28px 36px;
                margin: auto;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(66, 165, 245, 80))
        shadow.setOffset(0, 10)
        self.card_frame.setGraphicsEffect(shadow)

        self.card_layout = QVBoxLayout(self.card_frame)
        self.card_layout.setSpacing(18)

        # Theme toggle row
        theme_toggle_row = QHBoxLayout()
        self.theme_toggle = QCheckBox("🌙 Dark Mode")
        self.theme_toggle.setObjectName("themeToggle")
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        theme_toggle_row.addStretch()
        theme_toggle_row.addWidget(self.theme_toggle)
        self.card_layout.addLayout(theme_toggle_row)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search by tag, title or date...")
        self.search_bar.setObjectName("searchBar")
        self.search_bar.textChanged.connect(self.filter_entries)
        self.card_layout.addWidget(self.search_bar)

        # Entry list
        self.entry_list = QListWidget()
        self.entry_list.setObjectName("entryList")
        self.card_layout.addWidget(self.entry_list)

        # Action buttons row
        button_row = QHBoxLayout()
        button_row.setSpacing(18)

        mood_btn = QPushButton("📅\nMood\nTracker")
        calendar_btn = QPushButton("📆\nView\nCalendar")
        stats_btn = QPushButton("📈\nEntry\nStats")
        open_btn = QPushButton("🔓\nOpen\nEntry")
        new_btn = QPushButton("➕\nNew\nEntry")
        delete_btn = QPushButton("🗑️\nDelete\nEntry")
        change_pw_btn = QPushButton("🔐\nChange\nPassword")
        logout_btn = QPushButton("🚪\nLogout")

        # Connect signals
        mood_btn.clicked.connect(self.open_mood_tracker)
        calendar_btn.clicked.connect(self.open_entry_calendar)
        stats_btn.clicked.connect(self.open_stats)
        open_btn.clicked.connect(self.open_entry)
        new_btn.clicked.connect(self.new_entry)
        delete_btn.clicked.connect(self.delete_entry)
        change_pw_btn.clicked.connect(self.change_password)
        logout_btn.clicked.connect(self.logout)

        # Set better button design (multi-line, fixed width, elide text if needed)
        for btn in [mood_btn, calendar_btn, stats_btn, open_btn, new_btn, delete_btn, change_pw_btn, logout_btn]:
            btn.setObjectName("dashboardBtn")
            btn.setMinimumHeight(64)
            btn.setMaximumHeight(72)
            btn.setMinimumWidth(90)
            btn.setMaximumWidth(110)
            btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 15px;
                    font-weight: bold;
                    padding: 8px 6px;
                    border-radius: 14px;
                    background-color: #1976d2;
                    color: #fff;
                    border: none;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #1565c0;
                }
            """)
            button_row.addWidget(btn)

        self.card_layout.addLayout(button_row)

        self.main_layout.addWidget(self.card_frame, alignment=Qt.AlignHCenter)
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.main_layout)
        self.apply_dynamic_styles()
        self.load_entries()

    def resizeEvent(self, event):
        self.apply_dynamic_styles()
        return super().resizeEvent(event)

    def toggle_theme(self):
        # Toggle theme and reapply styles
        if self.theme == "light":
            self.theme = "dark"
        else:
            self.theme = "light"
        self.apply_dynamic_styles()

    def apply_dynamic_styles(self):
        w = max(self.width(), 900)
        h = max(self.height(), 600)
        scale = min(w / 1200, h / 800)
        scale = max(0.7, min(scale, 1.5))

        if self.theme == "dark":
            bg_grad = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460)"
            card_grad = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #23243a, stop:1 #2d3250)"
            title_color = "#90caf9"
            label_color = "#e6e6e6"
            input_bg = "#23243a"
            input_border = "#42a5f5"
            input_text = "#e6e6e6"
            list_bg = "#23243a"
            list_border = "#42a5f5"
        else:
            bg_grad = "#e3f2fd"
            card_grad = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e3f2fd, stop:0.5 #90caf9, stop:1 #42a5f5)"
            title_color = "#1976d2"
            label_color = "#333"
            input_bg = "#f5fafd"
            input_border = "#1976d2"
            input_text = "#222"
            list_bg = "#f5fafd"
            list_border = "#90caf9"

        self.setStyleSheet(f"background: {bg_grad};")
        self.card_frame.setMaximumWidth(int(self.width() * 0.98))
        self.title.setStyleSheet(f"""
            font-size: 36px;
            font-weight: bold;
            color: {title_color};
            margin-bottom: {int(8 * scale)}px;
            background: transparent;
        """)
        self.theme_toggle.setStyleSheet(f"""
            QCheckBox {{
                font-size: 16px;
                color: {label_color};
                background: transparent;
            }}
        """)
        self.search_bar.setStyleSheet(f"""
            padding: 12px;
            border: 2px solid {input_border};
            border-radius: 10px;
            font-size: 16px;
            background: {input_bg};
            color: {input_text};
        """)
        self.entry_list.setStyleSheet(f"""
            QListWidget {{
                background: {list_bg};
                border: 2px solid {list_border};
                border-radius: 12px;
                font-size: 15px;
                padding: 8px;
                color: {input_text};
            }}
        """)
        self.card_frame.setStyleSheet(f"""
            QFrame#dashboardCard {{
                background: {card_grad};
                border-radius: 22px;
                padding: 36px 36px 28px 36px;
                margin: auto;
            }}
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