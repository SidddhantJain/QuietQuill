from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QDesktopWidget
)
from PyQt5.QtCore import Qt
import sqlite3
import hashlib
from ui.dashboard import DashboardWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuietQuill - Login")

        # Set window size to 40% of the screen width and 50% of the screen height
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.4)
        height = int(screen.height() * 0.5)
        self.setGeometry(
            (screen.width() - width) // 2,
            (screen.height() - height) // 2,
            width,
            height
        )

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)

        # Title
        title = QLabel("🖋️ <i><b>QuietQuill</b></i>")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 16em;  /* Responsive font size */
            font-weight: bold;
            color: #4CBF52;
            margin-bottom: 30px;
        """)

        # Username Input
        username_layout = QVBoxLayout()
        username_label = QLabel("Username")
        username_label.setStyleSheet("""
            font-size: 1.5em;  /* Responsive font size */
            color: #333;
            margin-bottom: 5px;
        """)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            padding: 10px;
            border: 2px solid #4CAF50;
            border-radius: 6px;
            font-size: 1.2em;  /* Responsive font size */
        """)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)

        # Password Input
        password_layout = QVBoxLayout()
        password_label = QLabel("Password")
        password_label.setStyleSheet("""
            font-size: 1.5em;  /* Responsive font size */
            color: #333;
            margin-bottom: 5px;
        """)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            padding: 10px;
            border: 2px solid #4CAF50;
            border-radius: 6px;
            font-size: 1.2em;  /* Responsive font size */
        """)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)

        # Login Button
        self.login_btn = QPushButton("🔐 Login")
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 1.5em;  /* Responsive font size */
                padding: 12px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)

        # Register Link
        self.register_link = QPushButton("Don't have an account? Register")
        self.register_link.setStyleSheet("""
            QPushButton {
                border: none;
                color: #007BFF;
                text-decoration: underline;
                font-size: 1.2em;  /* Responsive font size */
            }
            QPushButton:hover {
                color: #0056b3;
            }
        """)
        self.register_link.setCursor(Qt.PointingHandCursor)
        self.register_link.clicked.connect(self.open_register)

        # Add widgets to layout
        layout.addWidget(title)
        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addSpacing(20)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_link, alignment=Qt.AlignCenter)

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
