from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDesktopWidget
)
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient
from PyQt5.QtCore import Qt
import sqlite3
import hashlib
import os
import binascii

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuietQuill - Register")

        # Set window size to 80% of the screen
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.4)
        height = int(screen.height() * 0.5)
        self.setGeometry(
            (screen.width() - width) // 2,
            (screen.height() - height) // 2,
            width,
            height
        )

        # Apply gradient background
        self.set_gradient_background()

        self.setup_ui()

    def set_gradient_background(self):
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, Qt.white)
        gradient.setColorAt(1, Qt.lightGray)
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Title
        title = QLabel("<h1 style='color: #4CAF50;'>Create Your Account</h1>")
        title.setAlignment(Qt.AlignCenter)

        # Username Input
        username_label = QLabel("Username")
        username_label.setStyleSheet("font-size: 1.5em; color: #333; margin-bottom: 5px;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a Username")
        self.username_input.setStyleSheet("""
            padding: 5px;
            border: 2px solid #4CAF50;
            border-radius: 6px;
            font-size: 1.2em;
        """)

        # Password Input
        password_label = QLabel("Password")
        password_label.setStyleSheet("font-size: 1.5em; color: #333; margin-bottom: 5px;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            padding: 10px;
            border: 2px solid #4CAF50;
            border-radius: 6px;
            font-size: 1.2em;
        """)

        # Confirm Password Input
        confirm_label = QLabel("Confirm Password")
        confirm_label.setStyleSheet("font-size: 1.5em; color: #333; margin-bottom: 5px;")
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm Password")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setStyleSheet("""
            padding: 10px;
            border: 2px solid #4CAF50;
            border-radius: 6px;
            font-size: 1.2em;
        """)

        # Register Button
        self.register_btn = QPushButton("Register")
        self.register_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 1.5em;
                padding: 12px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.register_btn.clicked.connect(self.handle_register)

        # Back to Login Button
        self.back_btn = QPushButton("Back to Login")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                font-size: 1.2em;
                padding: 10px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.back_btn.clicked.connect(self.back_to_login)

        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(confirm_label)
        layout.addWidget(self.confirm_input)
        layout.addSpacing(20)
        layout.addWidget(self.register_btn)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)

    def handle_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()

        if not username or not password or not confirm:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        salt = binascii.hexlify(os.urandom(16)).decode()
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()

        try:
            conn = sqlite3.connect("db/users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                           (username, password_hash, salt))
            conn.commit()
            conn.close()

            os.makedirs(f"entries/{username}", exist_ok=True)

            QMessageBox.information(self, "Success", "Account created successfully!")
            self.back_to_login()

        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists.")

    def back_to_login(self):
        from ui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
