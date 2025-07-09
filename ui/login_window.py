from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
import sqlite3
import hashlib
from ui.dashboard import DashboardWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuietQuill - Login")
        self.setGeometry(200, 150, 400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🖋️ <b>QuietQuill</b> - Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; margin-bottom: 20px;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("🔐 Login")
        self.login_btn.clicked.connect(self.handle_login)

        self.register_link = QPushButton("Don't have an account? Register")
        self.register_link.setStyleSheet("QPushButton { border: none; color: blue; text-decoration: underline; }")
        self.register_link.setCursor(Qt.PointingHandCursor)
        self.register_link.clicked.connect(self.open_register)

        layout.addWidget(title)
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password_input)
        layout.addSpacing(10)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_link, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        try:
            conn = sqlite3.connect("db/users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            conn.close()

            if result:
                stored_hash, salt = result
                input_hash = hashlib.sha256((password + salt).encode()).hexdigest()
                if input_hash == stored_hash:
                    print("✅ Login successful — opening Dashboard...")
                    self.dashboard = DashboardWindow(username)
                    self.dashboard.show()
                    self.close()
                else:
                    QMessageBox.warning(self, "Login Failed", "Incorrect password.")
            else:
                QMessageBox.warning(self, "Login Failed", "User not found.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Something went wrong: {str(e)}")

    def open_register(self):
        from ui.register_window import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()
