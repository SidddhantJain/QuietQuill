"""
User Registration Window Module

This module provides a PyQt5-based registration window for the QuietQuill application.
It handles user account creation with secure password hashing and validation.
"""

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
    """
    A PyQt5 widget for user registration with modern UI design.
    
    This window provides a registration form with the following features:
    - Username and password input fields
    - Password confirmation validation
    - Secure password hashing with salt
    - Responsive design with gradient styling
    - Database integration for user storage
    - Automatic user directory creation
    
    The window uses a card-based design with gradient backgrounds and shadow effects
    for a modern, professional appearance.
    """
    
    def __init__(self):
        """
        Initialize the RegisterWindow with default settings and UI setup.
        
        Sets up the window properties, centers it on screen, and initializes
        the user interface components.
        """
        super().__init__()
        self.setWindowTitle("QuietQuill - Register")
        self.setMinimumSize(420, 520)

        # Center the window on the screen
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
        """
        Set up the user interface components and layout.
        
        Creates and configures all UI elements including:
        - Main layout with proper spacing
        - Title label with styling
        - Card frame with gradient background and shadow
        - Input fields for username and passwords
        - Action buttons for registration and navigation
        """
        # Main layout setup with no margins for full-screen gradient effect
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Application title with emoji and bold styling
        self.title = QLabel("📝 <b>Create Your Account</b>")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("registerTitle")
        self.main_layout.addWidget(self.title, alignment=Qt.AlignHCenter)
        self.main_layout.addSpacing(8)

        # Card frame with gradient background and drop shadow for modern look
        self.card_frame = QFrame()
        self.card_frame.setObjectName("registerCard")
        # CSS-like styling for gradient background from light green to cyan
        self.card_frame.setStyleSheet("""
            QFrame#registerCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e3ffe6, stop:1 #b2f7ef);
                border-radius: 22px;
                padding: 36px 36px 28px 36px;
                margin: auto;
            }
        """)
        # Drop shadow effect for depth and modern appearance
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(76, 191, 82, 80))  # Semi-transparent green shadow
        shadow.setOffset(0, 10)  # Slight vertical offset for depth
        self.card_frame.setGraphicsEffect(shadow)

        # Card layout for organizing form elements
        self.card_layout = QVBoxLayout(self.card_frame)
        self.card_layout.setSpacing(18)

        # Username input field with label
        username_label = QLabel("Username")
        username_label.setStyleSheet("font-size: 17px; color: #333; margin-bottom: 5px;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a Username")
        self.username_input.setObjectName("usernameInput")

        # Password input field with hidden text for security
        password_label = QLabel("Password")
        password_label.setStyleSheet("font-size: 17px; color: #333; margin-bottom: 5px;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password characters
        self.password_input.setObjectName("passwordInput")

        # Password confirmation field to prevent typos
        confirm_label = QLabel("Confirm Password")
        confirm_label.setStyleSheet("font-size: 17px; color: #333; margin-bottom: 5px;")
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm Password")
        self.confirm_input.setEchoMode(QLineEdit.Password)  # Hide password characters
        self.confirm_input.setObjectName("confirmInput")

        # Primary action button for registration
        self.register_btn = QPushButton("Register")
        self.register_btn.setObjectName("registerBtn")
        self.register_btn.clicked.connect(self.handle_register)

        # Secondary action button for navigation back to login
        self.back_btn = QPushButton("Back to Login")
        self.back_btn.setObjectName("backBtn")
        self.back_btn.clicked.connect(self.back_to_login)

        # Add all form elements to the card layout
        self.card_layout.addWidget(username_label)
        self.card_layout.addWidget(self.username_input)
        self.card_layout.addWidget(password_label)
        self.card_layout.addWidget(self.password_input)
        self.card_layout.addWidget(confirm_label)
        self.card_layout.addWidget(self.confirm_input)
        self.card_layout.addSpacing(18)  # Extra spacing before buttons
        self.card_layout.addWidget(self.register_btn)
        self.card_layout.addWidget(self.back_btn)

        # Add card to main layout with center alignment
        self.main_layout.addWidget(self.card_frame, alignment=Qt.AlignHCenter)
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.main_layout)
        self.apply_dynamic_styles()

    def resizeEvent(self, event):
        """
        Handle window resize events to maintain responsive design.
        
        Args:
            event: The resize event containing new window dimensions
        """
        # Reapply styles when window is resized for responsive design
        self.apply_dynamic_styles()
        return super().resizeEvent(event)

    def apply_dynamic_styles(self):
        """
        Apply responsive styling based on current window dimensions.
        
        This method calculates scaling factors based on window size and applies
        appropriate font sizes, padding, and other style properties to maintain
        a consistent appearance across different screen sizes.
        """
        # Calculate scaling based on window dimensions with minimum constraints
        w = max(self.width(), 420)
        h = max(self.height(), 520)
        scale = min(w / 600, h / 700)
        scale = max(0.8, min(scale, 1.3))  # Clamp scale between 0.8 and 1.3
        
        # Set maximum card width based on window width
        self.card_frame.setMaximumWidth(int(self.width() * 0.98))
        
        # Scale title font size and styling
        self.title.setStyleSheet(f"""
            font-size: {int(32 * scale)}px;
            font-weight: bold;
            color: #4CBF52;
            margin-bottom: {int(8 * scale)}px;
            background: transparent;
        """)
        
        # Scale input field styling for all text inputs
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
        
        # Scale register button with hover effects
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
        
        # Scale back button with different color scheme
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
        
        # Scale card frame padding and border radius
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
        """
        Handle user registration process with validation and secure storage.
        
        This method performs the following operations:
        1. Validates all input fields are filled
        2. Confirms password match
        3. Generates secure password hash with salt
        4. Stores user data in SQLite database
        5. Creates user directory for entries
        6. Provides user feedback and navigation
        """
        # Get and sanitize input values
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()

        # Validate all required fields are filled
        if not username or not password or not confirm:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        # Ensure password confirmation matches
        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        # Generate cryptographically secure salt for password hashing
        salt = binascii.hexlify(os.urandom(16)).decode()
        # Create secure password hash using SHA-256 with salt
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()

        try:
            # Database transaction for user creation
            conn = sqlite3.connect("db/users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                           (username, password_hash, salt))
            conn.commit()
            conn.close()

            # Create user-specific directory for storing journal entries
            os.makedirs(f"entries/{username}", exist_ok=True)

            # Show success message and navigate to login
            QMessageBox.information(self, "Success", "Account created successfully!")
            self.back_to_login()

        except sqlite3.IntegrityError:
            # Handle duplicate username error
            QMessageBox.warning(self, "Error", "Username already exists.")

    def back_to_login(self):
        """
        Navigate back to the login window.
        
        Creates a new LoginWindow instance, displays it, and closes
        the current registration window.
        """
        # Import here to avoid circular imports
        from ui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
