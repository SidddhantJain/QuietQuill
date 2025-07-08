from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
import sqlite3
import hashlib
import os
import binascii

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuietQuill - Register")
        self.setGeometry(100, 100, 300, 250)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm Password")
        self.confirm_input.setEchoMode(QLineEdit.Password)

        self.register_btn = QPushButton("Register")
        self.register_btn.clicked.connect(self.handle_register)

        self.back_btn = QPushButton("Back to Login")
        self.back_btn.clicked.connect(self.back_to_login)

        layout.addWidget(QLabel("<h2>Create Your Account</h2>"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_input)
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
