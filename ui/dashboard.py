import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from ui.editor import EditorWindow


class DashboardWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"QuietQuill - Dashboard ({self.username})")
        self.setGeometry(200, 150, 600, 400)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # Title
        title = QLabel(f"📔 Welcome, <b>{self.username}</b>")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; margin-bottom: 15px;")
        main_layout.addWidget(title)

        # Entry List
        self.entry_list = QListWidget()
        self.load_entries()
        main_layout.addWidget(self.entry_list)

        # Buttons
        open_btn = QPushButton("🔓 Open Entry")
        open_btn.clicked.connect(self.open_entry)

        new_btn = QPushButton("➕ New Entry")
        new_btn.clicked.connect(self.new_entry)

        logout_btn = QPushButton("🚪 Logout")
        logout_btn.clicked.connect(self.logout)

        button_row = QHBoxLayout()
        button_row.addWidget(open_btn)
        button_row.addWidget(new_btn)
        button_row.addWidget(logout_btn)

        main_layout.addLayout(button_row)
        self.setLayout(main_layout)

    def load_entries(self):
        entry_dir = os.path.join("entries", self.username)
        os.makedirs(entry_dir, exist_ok=True)
        files = [f for f in os.listdir(entry_dir) if f.endswith(".enc")]
        self.entry_list.clear()
        self.entry_list.addItems(sorted(files))

    def open_entry(self):
        selected = self.entry_list.currentItem()
        if selected:
            filename = selected.text()
            self.editor = EditorWindow(self.username, filename)
            self.editor.show()
        else:
            QMessageBox.warning(self, "No Selection", "Please select an entry to open.")

    def new_entry(self):
        self.editor = EditorWindow(self.username)
        self.editor.show()

    def logout(self):
        from ui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
