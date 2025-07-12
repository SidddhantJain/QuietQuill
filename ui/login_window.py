"""
Login Window Module

This module provides the main login interface for the QuietQuill application.
It handles user authentication with secure password verification and provides
navigation to registration for new users.
"""

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
    """
    A PyQt5 widget for user authentication with modern UI design.
    
    This window provides a login form with the following features:
    - Username and password input fields
    - Secure password verification using SHA-256 hashing
    - Responsive design with gradient styling and shadow effects
    - Navigation to registration window for new users
    - Database integration for user authentication
    - Error handling and user feedback
    
    The window uses a card-based design with gradient backgrounds and shadow effects
    for a modern, professional appearance that scales responsively.
    
    Attributes:
        title (QLabel): Application title display
        form_frame (QFrame): Container for the login form with styling
        username_input (QLineEdit): Username input field
        password_input (QLineEdit): Password input field with hidden text
        login_btn (QPushButton): Primary login action button
        register_link (QPushButton): Link to registration window
    """
    
    def __init__(self):
        """
        Initialize the LoginWindow with default settings and UI setup.
        
        Sets up the window properties, applies base styling, and initializes
        all user interface components.
        """
        super().__init__()
        self.setWindowTitle("QuietQuill - Login")
        self.setMinimumSize(350, 320)
        
        # Set base background color for the entire window
        self.setStyleSheet("""
            QWidget {
                background-color: #e8f5e9;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface components and layout.
        
        Creates and configures all UI elements including:
        - Main layout with proper spacing and margins
        - Application title with brand styling
        - Form frame with gradient background and shadow
        - Input fields for username and password
        - Action buttons for login and registration navigation
        """
        # Main layout setup with no margins for full-screen background effect
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Application title with emoji and brand styling
        self.title = QLabel("🖋️ <b>QuietQuill</b>")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("titleLabel")
        self.main_layout.addWidget(self.title, alignment=Qt.AlignHCenter)
        self.main_layout.addSpacing(8)

        # Form container with gradient background and shadow for modern look
        self.form_frame = QFrame()
        self.form_frame.setObjectName("formFrame")
        # CSS-like styling for gradient background from white to light green
        self.form_frame.setStyleSheet("""
            QFrame#formFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff, stop:1 #f1f8e9);
                border-radius: 18px;
                padding: 32px 32px 24px 32px;
                margin: auto;
            }
        """)
        
        # Drop shadow effect for depth and modern appearance
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setColor(QColor(76, 191, 82, 80))  # Semi-transparent green shadow
        shadow.setOffset(0, 6)  # Slight vertical offset for depth
        self.form_frame.setGraphicsEffect(shadow)

        # Form layout for organizing input elements
        self.form_layout = QVBoxLayout(self.form_frame)
        self.form_layout.setSpacing(18)

        # Username input section
        self.username_label = QLabel("Username")
        self.username_label.setObjectName("usernameLabel")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setObjectName("usernameInput")
        self.form_layout.addWidget(self.username_label)
        self.form_layout.addWidget(self.username_input)

        # Password input section with hidden text for security
        self.password_label = QLabel("Password")
        self.password_label.setObjectName("passwordLabel")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password characters
        self.password_input.setObjectName("passwordInput")
        self.form_layout.addWidget(self.password_label)
        self.form_layout.addWidget(self.password_input)

        # Primary login action button
        self.login_btn = QPushButton("🔐 Login")
        self.login_btn.setObjectName("loginBtn")
        self.login_btn.clicked.connect(self.handle_login)
        self.form_layout.addWidget(self.login_btn)

        # Registration navigation link styled as button
        self.register_link = QPushButton("Don't have an account? Register")
        self.register_link.setObjectName("registerLink")
        self.register_link.setCursor(Qt.PointingHandCursor)  # Hand cursor for link feel
        self.register_link.clicked.connect(self.open_register)
        self.form_layout.addWidget(self.register_link, alignment=Qt.AlignCenter)

        # Add form to main layout and apply responsive styling
        self.main_layout.addWidget(self.form_frame, alignment=Qt.AlignHCenter)
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
        w = max(self.width(), 350)
        h = max(self.height(), 320)
        scale = min(w / 500, h / 400)
        scale = max(0.7, min(scale, 1.5))  # Clamp scale between 0.7 and 1.5
        
        # Set maximum form width based on window width
        self.form_frame.setMaximumWidth(int(self.width() * 0.95))
        
        # Scale title font size and styling
        self.title.setStyleSheet(f"""
            font-size: {int(32 * scale)}px;
            font-weight: bold;
            color: #4CBF52;
            margin-bottom: {int(6 * scale)}px;
            background: transparent;
        """)
        
        # Scale label styling for consistent appearance
        label_style = f"font-size: {int(16 * scale)}px; color: #333; background: transparent;"
        self.username_label.setStyleSheet(label_style)
        self.password_label.setStyleSheet(label_style)
        
        # Scale input field styling with consistent borders
        input_style = f"""
            padding: {int(10 * scale)}px;
            border: 2px solid #4CBF52;
            border-radius: {int(8 * scale)}px;
            font-size: {int(15 * scale)}px;
        """
        self.username_input.setStyleSheet(input_style)
        self.password_input.setStyleSheet(input_style)
        
        # Scale login button with hover effects
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
        
        # Scale registration link with underline effect
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
        
        # Scale form frame with updated gradient and padding
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
        """
        Handle user login authentication process.
        
        This method performs the following operations:
        1. Validates input fields are not empty
        2. Queries database for user credentials
        3. Verifies password using secure hashing
        4. Opens dashboard on successful authentication
        5. Provides appropriate error messages for failures
        """
        # Get and sanitize input values
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # Validate required fields are filled
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        try:
            # Database query to retrieve user credentials
            conn = sqlite3.connect("db/users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            conn.close()

            if result:
                # Verify password using stored hash and salt
                stored_hash, salt = result
                input_hash = hashlib.sha256((password + salt).encode()).hexdigest()
                
                if input_hash == stored_hash:
                    # Successful authentication - open dashboard
                    print("✅ Login successful — opening Dashboard...")
                    self.dashboard = DashboardWindow(username)
                    self.dashboard.show()
                    self.close()
                else:
                    # Password verification failed
                    QMessageBox.warning(self, "Login Failed", "Incorrect password.")
            else:
                # User not found in database
                QMessageBox.warning(self, "Login Failed", "User not found.")
                
        except Exception as e:
            # Handle database or other unexpected errors
            QMessageBox.critical(self, "Error", f"Something went wrong: {str(e)}")

    def open_register(self):
        """
        Navigate to the registration window.
        
        Creates a new RegisterWindow instance, displays it, and closes
        the current login window. Uses late import to avoid circular imports.
        """
        # Import here to avoid circular imports
        from ui.register_window import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()
