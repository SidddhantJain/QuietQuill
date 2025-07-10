from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDesktopWidget,
    QFrame, QSpacerItem, QSizePolicy, QHBoxLayout, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor, QFont
from PyQt5.QtCore import Qt
import sqlite3
import hashlib
import os
import binascii

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuietQuill - Register")
        self.setMinimumSize(420, 520)

        # Center window
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
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Title above the card
        self.title = QLabel("📝 <b>Create Your Account</b>")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("registerTitle")
        self.main_layout.addWidget(self.title, alignment=Qt.AlignHCenter)
        self.main_layout.addSpacing(8)

        # Card frame with gradient and shadow
        self.card_frame = QFrame()
        self.card_frame.setObjectName("registerCard")
        self.card_frame.setStyleSheet("""
            QFrame#registerCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e3ffe6, stop:1 #b2f7ef);
                border-radius: 22px;
                padding: 36px 36px 28px 36px;
                margin: auto;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(76, 191, 82, 80))
        shadow.setOffset(0, 10)
        self.card_frame.setGraphicsEffect(shadow)

        self.card_layout = QVBoxLayout(self.card_frame)
        self.card_layout.setSpacing(18)

        # Username Input
        username_label = QLabel("Username")
        username_label.setStyleSheet("font-size: 17px; color: #333; margin-bottom: 5px;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a Username")
        self.username_input.setObjectName("usernameInput")

        # Password Input
        password_label = QLabel("Password")
        password_label.setStyleSheet("font-size: 17px; color: #333; margin-bottom: 5px;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("passwordInput")

        # Confirm Password Input
        confirm_label = QLabel("Confirm Password")
        confirm_label.setStyleSheet("font-size: 17px; color: #333; margin-bottom: 5px;")
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm Password")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setObjectName("confirmInput")

        # Register Button
        self.register_btn = QPushButton("Register")
        self.register_btn.setObjectName("registerBtn")
        self.register_btn.clicked.connect(self.handle_register)

        # Back to Login Button
        self.back_btn = QPushButton("Back to Login")
        self.back_btn.setObjectName("backBtn")
        self.back_btn.clicked.connect(self.back_to_login)

        # Add widgets to card layout
        self.card_layout.addWidget(username_label)
        self.card_layout.addWidget(self.username_input)
        self.card_layout.addWidget(password_label)
        self.card_layout.addWidget(self.password_input)
        self.card_layout.addWidget(confirm_label)
        self.card_layout.addWidget(self.confirm_input)
        self.card_layout.addSpacing(18)
        self.card_layout.addWidget(self.register_btn)
        self.card_layout.addWidget(self.back_btn)

        self.main_layout.addWidget(self.card_frame, alignment=Qt.AlignHCenter)
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.main_layout)
        self.apply_dynamic_styles()

    def resizeEvent(self, event):
        self.apply_dynamic_styles()
        return super().resizeEvent(event)

    def apply_dynamic_styles(self):
        w = max(self.width(), 420)
        h = max(self.height(), 520)
        scale = min(w / 600, h / 700)
        scale = max(0.8, min(scale, 1.3))
        self.card_frame.setMaximumWidth(int(self.width() * 0.98))
        self.title.setStyleSheet(f"""
            font-size: {int(32 * scale)}px;
            font-weight: bold;
            color: #4CBF52;
            margin-bottom: {int(8 * scale)}px;
            background: transparent;
        """)
        for objname in ["usernameInput", "passwordInput", "confirmInput"]:
            widget = self.findChild(QLineEdit, objname)
            if widget:
                widget.setStyleSheet(f"""
                    QLineEdit {{
                        padding: {int(10 * scale)}px;
                        border: 2px solid #4CBF52;
                        border-radius: {int(8 * scale)}px;
                        font-size: {int(16 * scale)}px;
                    }}
                """)
        self.register_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #4CBF52;
                color: white;
                font-size: {int(18 * scale)}px;
                padding: {int(12 * scale)}px;
                border: none;
                border-radius: {int(8 * scale)}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #388e3c;
            }}
        """)
        self.back_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #007BFF;
                color: white;
                font-size: {int(15 * scale)}px;
                padding: {int(10 * scale)}px;
                border: none;
                border-radius: {int(8 * scale)}px;
            }}
            QPushButton:hover {{
                background-color: #0056b3;
            }}
        """)
        self.card_frame.setStyleSheet(f"""
            QFrame#registerCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #e3ffe6, stop:1 #b2f7ef);
                border-radius: {int(22 * scale)}px;
                padding: {int(36 * scale)}px {int(36 * scale)}px {int(28 * scale)}px {int(36 * scale)}px;
                margin: auto;
            }}
        """)

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
