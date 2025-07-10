from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QDesktopWidget, QSpacerItem, QSizePolicy, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
import sqlite3
import hashlib
from ui.dashboard import DashboardWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuietQuill - Login")
        self.setMinimumSize(350, 320)
        self.setStyleSheet("""
            QWidget {
                background-color: #e8f5e9;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Title above the form box
        self.title = QLabel("🖋️ <b>QuietQuill</b>")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("titleLabel")
        self.main_layout.addWidget(self.title, alignment=Qt.AlignHCenter)
        self.main_layout.addSpacing(8)

        self.form_frame = QFrame()
        self.form_frame.setObjectName("formFrame")
        # Gradient background for the form box
        self.form_frame.setStyleSheet("""
            QFrame#formFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff, stop:1 #f1f8e9);
                border-radius: 18px;
                padding: 32px 32px 24px 32px;
                margin: auto;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setColor(QColor(76, 191, 82, 80))
        shadow.setOffset(0, 6)
        self.form_frame.setGraphicsEffect(shadow)

        self.form_layout = QVBoxLayout(self.form_frame)
        self.form_layout.setSpacing(18)

        self.username_label = QLabel("Username")
        self.username_label.setObjectName("usernameLabel")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setObjectName("usernameInput")
        self.form_layout.addWidget(self.username_label)
        self.form_layout.addWidget(self.username_input)

        self.password_label = QLabel("Password")
        self.password_label.setObjectName("passwordLabel")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("passwordInput")
        self.form_layout.addWidget(self.password_label)
        self.form_layout.addWidget(self.password_input)

        self.login_btn = QPushButton("🔐 Login")
        self.login_btn.setObjectName("loginBtn")
        self.login_btn.clicked.connect(self.handle_login)
        self.form_layout.addWidget(self.login_btn)

        self.register_link = QPushButton("Don't have an account? Register")
        self.register_link.setObjectName("registerLink")
        self.register_link.setCursor(Qt.PointingHandCursor)
        self.register_link.clicked.connect(self.open_register)
        self.form_layout.addWidget(self.register_link, alignment=Qt.AlignCenter)

        self.main_layout.addWidget(self.form_frame, alignment=Qt.AlignHCenter)
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.main_layout)
        self.apply_dynamic_styles()

    def resizeEvent(self, event):
        self.apply_dynamic_styles()
        return super().resizeEvent(event)

    def apply_dynamic_styles(self):
        w = max(self.width(), 350)
        h = max(self.height(), 320)
        scale = min(w / 500, h / 400)
        scale = max(0.7, min(scale, 1.5))
        self.form_frame.setMaximumWidth(int(self.width() * 0.95))
        # Title font, no background
        self.title.setStyleSheet(f"""
            font-size: {int(32 * scale)}px;
            font-weight: bold;
            color: #4CBF52;
            margin-bottom: {int(6 * scale)}px;
            background: transparent;
        """)
        label_style = f"font-size: {int(16 * scale)}px; color: #333; background: transparent;"
        self.username_label.setStyleSheet(label_style)
        self.password_label.setStyleSheet(label_style)
        input_style = f"""
            padding: {int(10 * scale)}px;
            border: 2px solid #4CBF52;
            border-radius: {int(8 * scale)}px;
            font-size: {int(15 * scale)}px;
        """
        self.username_input.setStyleSheet(input_style)
        self.password_input.setStyleSheet(input_style)
        self.login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #4CBF52;
                color: white;
                font-size: {int(18 * scale)}px;
                padding: {int(12 * scale)}px;
                border: none;
                border-radius: {int(8 * scale)}px;
            }}
            QPushButton:hover {{
                background-color: #388e3c;
            }}
        """)
        self.register_link.setStyleSheet(f"""
            QPushButton {{
                border: none;
                color: #007BFF;
                text-decoration: underline;
                font-size: {int(14 * scale)}px;
                background: transparent;
            }}
            QPushButton:hover {{
                color: #0056b3;
            }}
        """)
        self.form_frame.setStyleSheet(f"""
            QFrame#formFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #e3f2fd, stop:0.5 #90caf9, stop:1 #42a5f5);
                border-radius: {int(18 * scale)}px;
                padding: {int(32 * scale)}px {int(32 * scale)}px {int(24 * scale)}px {int(32 * scale)}px;
                margin: auto;
            }}
        """)

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
