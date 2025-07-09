import sqlite3
import hashlib
import uuid
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)


class ChangePasswordWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("🔐 Change Password")
        self.setGeometry(300, 200, 400, 250)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Current Password:"))
        self.old_pass = QLineEdit()
        self.old_pass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.old_pass)

        layout.addWidget(QLabel("New Password:"))
        self.new_pass = QLineEdit()
        self.new_pass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.new_pass)

        layout.addWidget(QLabel("Confirm New Password:"))
        self.confirm_pass = QLineEdit()
        self.confirm_pass.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_pass)

        save_btn = QPushButton("Update Password")
        save_btn.clicked.connect(self.update_password)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def update_password(self):
        old = self.old_pass.text()
        new = self.new_pass.text()
        confirm = self.confirm_pass.text()

        if not old or not new or not confirm:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if new != confirm:
            QMessageBox.warning(self, "Mismatch", "New passwords do not match.")
            return

        try:
            conn = sqlite3.connect("db/users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash, salt FROM users WHERE username = ?", (self.username,))
            result = cursor.fetchone()

            if result:
                stored_hash, salt = result
                input_old_hash = hashlib.sha256((old + salt).encode()).hexdigest()

                if input_old_hash == stored_hash:
                    new_salt = uuid.uuid4().hex
                    new_hash = hashlib.sha256((new + new_salt).encode()).hexdigest()
                    cursor.execute("UPDATE users SET password_hash = ?, salt = ? WHERE username = ?",
                                   (new_hash, new_salt, self.username))
                    conn.commit()
                    QMessageBox.information(self, "Success", "Password updated successfully.")
                    self.close()
                else:
                    QMessageBox.warning(self, "Error", "Incorrect current password.")
            else:
                QMessageBox.critical(self, "Error", "User not found.")
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
