"""
Dashboard Window Module

This module provides the main dashboard interface for the QuietQuill application.
It serves as the central hub for managing journal entries, accessing various features,
and navigating between different parts of the application.
"""

import os
import json
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget,
    QMessageBox, QHBoxLayout, QLineEdit, QDesktopWidget,
    QCheckBox, QSpacerItem, QSizePolicy, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from ui.editor import EditorWindow


class DashboardWindow(QWidget):
    """
    The main dashboard window for the QuietQuill application.
    
    This window provides a comprehensive interface for managing journal entries
    and accessing various application features including:
    - Entry listing and search functionality
    - Theme switching (light/dark mode)
    - Entry management (create, open, delete)
    - Navigation to specialized windows (mood tracker, calendar, stats)
    - User account management (password change, logout)
    - Responsive design with gradient styling
    
    The dashboard uses a card-based design with gradient backgrounds and shadow
    effects for a modern, professional appearance that adapts to different themes.
    
    Attributes:
        username (str): The current user's username
        theme (str): Current UI theme ("light" or "dark")
        title (QLabel): Welcome message display
        card_frame (QFrame): Main content container with styling
        theme_toggle (QCheckBox): Dark mode toggle switch
        search_bar (QLineEdit): Entry search input field
        entry_list (QListWidget): List of user's journal entries
        all_entries (list): Complete list of entries for filtering
    """
    
    def __init__(self, username):
        """
        Initialize the DashboardWindow for a specific user.
        
        Args:
            username (str): The username of the current user
        """
        super().__init__()
        self.username = username
        self.theme = "light"  # Default theme setting
        self.setWindowTitle(f"QuietQuill - Dashboard ({self.username})")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background-color: #e3f2fd;")
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface components and layout.
        
        Creates and configures all UI elements including:
        - Main layout with card-based design
        - Welcome title with user's name
        - Theme toggle for light/dark mode switching
        - Search bar for entry filtering
        - Entry list for displaying journal entries
        - Action buttons for various operations
        - Responsive styling and event connections
        """
        # Main layout setup with no margins for full-screen gradient effect
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Welcome title with user's name
        self.title = QLabel(f"📔 <b>Welcome, {self.username}</b>")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("dashboardTitle")
        self.main_layout.addWidget(self.title, alignment=Qt.AlignHCenter)
        self.main_layout.addSpacing(8)

        # Card frame with gradient background and drop shadow for modern look
        self.card_frame = QFrame()
        self.card_frame.setObjectName("dashboardCard")
        # CSS-like styling for gradient background from white to light blue
        self.card_frame.setStyleSheet("""
            QFrame#dashboardCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff, stop:1 #e3f2fd);
                border-radius: 22px;
                padding: 36px 36px 28px 36px;
                margin: auto;
            }
        """)
        # Drop shadow effect for depth and modern appearance
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(66, 165, 245, 80))  # Semi-transparent blue shadow
        shadow.setOffset(0, 10)  # Slight vertical offset for depth
        self.card_frame.setGraphicsEffect(shadow)

        # Card layout for organizing dashboard components
        self.card_layout = QVBoxLayout(self.card_frame)
        self.card_layout.setSpacing(18)

        # Theme toggle row for dark mode switching
        theme_toggle_row = QHBoxLayout()
        self.theme_toggle = QCheckBox("🌙 Dark Mode")
        self.theme_toggle.setObjectName("themeToggle")
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        theme_toggle_row.addStretch()  # Push toggle to the right
        theme_toggle_row.addWidget(self.theme_toggle)
        self.card_layout.addLayout(theme_toggle_row)

        # Search bar for filtering entries by various criteria
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search by tag, title or date...")
        self.search_bar.setObjectName("searchBar")
        self.search_bar.textChanged.connect(self.filter_entries)
        self.card_layout.addWidget(self.search_bar)

        # Entry list for displaying journal entries
        self.entry_list = QListWidget()
        self.entry_list.setObjectName("entryList")
        self.card_layout.addWidget(self.entry_list)

        # Action buttons row with various dashboard operations
        button_row = QHBoxLayout()
        button_row.setSpacing(18)

        # Create action buttons with icons and multi-line labels
        mood_btn = QPushButton("📅\nMood\nTracker")
        calendar_btn = QPushButton("📆\nView\nCalendar")
        stats_btn = QPushButton("📈\nEntry\nStats")
        open_btn = QPushButton("🔓\nOpen\nEntry")
        new_btn = QPushButton("➕\nNew\nEntry")
        delete_btn = QPushButton("🗑️\nDelete\nEntry")
        change_pw_btn = QPushButton("🔐\nChange\nPassword")
        logout_btn = QPushButton("🚪\nLogout")

        # Connect button signals to their respective handler methods
        mood_btn.clicked.connect(self.open_mood_tracker)
        calendar_btn.clicked.connect(self.open_entry_calendar)
        stats_btn.clicked.connect(self.open_stats)
        open_btn.clicked.connect(self.open_entry)
        new_btn.clicked.connect(self.new_entry)
        delete_btn.clicked.connect(self.delete_entry)
        change_pw_btn.clicked.connect(self.change_password)
        logout_btn.clicked.connect(self.logout)

        # Apply consistent styling to all action buttons
        for btn in [mood_btn, calendar_btn, stats_btn, open_btn, new_btn, delete_btn, change_pw_btn, logout_btn]:
            btn.setObjectName("dashboardBtn")
            btn.setMinimumHeight(64)
            btn.setMaximumHeight(72)
            btn.setMinimumWidth(90)
            btn.setMaximumWidth(110)
            btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 15px;
                    font-weight: bold;
                    padding: 8px 6px;
                    border-radius: 14px;
                    background-color: #1976d2;
                    color: #fff;
                    border: none;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #1565c0;
                }
            """)
            button_row.addWidget(btn)

        self.card_layout.addLayout(button_row)

        # Add card to main layout and finalize setup
        self.main_layout.addWidget(self.card_frame, alignment=Qt.AlignHCenter)
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.main_layout)
        self.apply_dynamic_styles()
        self.load_entries()

    def resizeEvent(self, event):
        """
        Handle window resize events to maintain responsive design.
        
        Args:
            event: The resize event containing new window dimensions
        """
        # Reapply styles when window is resized for responsive design
        self.apply_dynamic_styles()
        return super().resizeEvent(event)

    def toggle_theme(self):
        """
        Toggle between light and dark themes.
        
        Switches the current theme and reapplies all styling to reflect
        the new theme throughout the dashboard interface.
        """
        # Toggle theme state and reapply styles
        if self.theme == "light":
            self.theme = "dark"
        else:
            self.theme = "light"
        self.apply_dynamic_styles()

    def apply_dynamic_styles(self):
        """
        Apply responsive styling based on current theme and window dimensions.
        
        This method calculates appropriate styling for the current theme
        (light or dark) and applies it to all UI components. It handles
        color schemes, gradients, and responsive scaling.
        """
        # Calculate scaling factors for responsive design
        w = max(self.width(), 900)
        h = max(self.height(), 600)
        scale = min(w / 1200, h / 800)
        scale = max(0.7, min(scale, 1.5))

        # Define color schemes for different themes
        if self.theme == "dark":
            # Dark theme color palette
            bg_grad = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460)"
            card_grad = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #23243a, stop:1 #2d3250)"
            title_color = "#90caf9"
            label_color = "#e6e6e6"
            input_bg = "#23243a"
            input_border = "#42a5f5"
            input_text = "#e6e6e6"
            list_bg = "#23243a"
            list_border = "#42a5f5"
        else:
            # Light theme color palette
            bg_grad = "#e3f2fd"
            card_grad = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e3f2fd, stop:0.5 #90caf9, stop:1 #42a5f5)"
            title_color = "#1976d2"
            label_color = "#333"
            input_bg = "#f5fafd"
            input_border = "#1976d2"
            input_text = "#222"
            list_bg = "#f5fafd"
            list_border = "#90caf9"

        # Apply theme-specific styling to all components
        self.setStyleSheet(f"background: {bg_grad};")
        self.card_frame.setMaximumWidth(int(self.width() * 0.98))
        self.title.setStyleSheet(f"""
            font-size: 36px;
            font-weight: bold;
            color: {title_color};
            margin-bottom: {int(8 * scale)}px;
            background: transparent;
        """)
        self.theme_toggle.setStyleSheet(f"""
            QCheckBox {{
                font-size: 16px;
                color: {label_color};
                background: transparent;
            }}
        """)
        self.search_bar.setStyleSheet(f"""
            padding: 12px;
            border: 2px solid {input_border};
            border-radius: 10px;
            font-size: 16px;
            background: {input_bg};
            color: {input_text};
        """)
        self.entry_list.setStyleSheet(f"""
            QListWidget {{
                background: {list_bg};
                border: 2px solid {list_border};
                border-radius: 12px;
                font-size: 15px;
                padding: 8px;
                color: {input_text};
            }}
        """)
        self.card_frame.setStyleSheet(f"""
            QFrame#dashboardCard {{
                background: {card_grad};
                border-radius: 22px;
                padding: 36px 36px 28px 36px;
                margin: auto;
            }}
        """)

    def open_stats(self):
        """
        Open the statistics window to display entry analytics.
        
        Creates and displays a new StatsWindow instance showing
        various statistics about the user's journal entries.
        """
        from ui.stats import StatsWindow
        self.stats_window = StatsWindow(self.username)
        self.stats_window.show()

    def get_entry_dir(self):
        """
        Get the directory path for the current user's entries.
        
        Returns:
            str: The path to the user's entries directory
        """
        return os.path.join("entries", self.username)
    
    def open_entry_calendar(self):
        """
        Open the entry calendar window for date-based entry viewing.
        
        Creates and displays a new EntryCalendarWindow instance
        allowing the user to view entries by date on a calendar.
        """
        from ui.entry_calendar import EntryCalendarWindow
        self.calendar_window = EntryCalendarWindow(self.username)
        self.calendar_window.show()

    def open_mood_tracker(self):
        """
        Open the mood tracker window for emotional state tracking.
        
        Creates and displays a new MoodTrackerWindow instance
        allowing the user to track their mood over time.
        """
        from ui.mood_tracker import MoodTrackerWindow
        self.mood_window = MoodTrackerWindow(self.username)
        self.mood_window.show()

    def load_entries(self):
        """
        Load all journal entries for the current user.
        
        This method scans the user's entry directory recursively,
        loads metadata for each entry, and populates the entry list
        with formatted information including titles, timestamps, and tags.
        """
        self.entry_list.clear()
        self.all_entries = []  # Store all entries for filtering

        entry_path = self.get_entry_dir()
        # Recursively scan for encrypted entry files
        for root, _, files in os.walk(entry_path):
            for file in files:
                if file.endswith(".enc"):
                    # Look for corresponding metadata file
                    meta_file = file.replace(".enc", ".meta.json")
                    meta_path = os.path.join(root, meta_file)
                    if os.path.exists(meta_path):
                        try:
                            # Load metadata and create formatted label
                            with open(meta_path, "r") as f:
                                meta = json.load(f)
                                label = f"{meta.get('title')} | {meta.get('start_time')} → {meta.get('end_time', '---')}"
                                tags = meta.get("tags", [])
                                if tags:
                                    label += f"\nTags: {', '.join(tags)}"
                                self.all_entries.append((label, file))
                        except (json.JSONDecodeError, IOError):
                            # Use filename as fallback if metadata is corrupted
                            self.all_entries.append((file, file))
                    else:
                        # Use filename as fallback if no metadata exists
                        self.all_entries.append((file, file))
        self.refresh_entry_list()

    def new_entry(self):
        """
        Create a new journal entry.
        
        Opens a new EditorWindow instance for creating a new
        journal entry with the current theme settings.
        """
        self.editor = EditorWindow(self.username)
        self.editor.show()

    def open_entry(self):
        """
        Open the selected entry in the editor window.
        
        Gets the currently selected entry from the list and opens
        it in a new EditorWindow instance for viewing and editing.
        """
        selected = self.entry_list.currentItem()
        if selected:
            filename = selected.data(Qt.UserRole)
            self.editor = EditorWindow(self.username, filename=filename, theme=self.theme)
            self.editor.show()


    def refresh_entry_list(self):
        """
        Refresh the entry list display with current entries.
        
        Updates the QListWidget to show all entries from the
        all_entries list, used after filtering or loading.
        """
        self.entry_list.clear()
        for label, _ in self.all_entries:
            self.entry_list.addItem(label)

    def filter_entries(self, text):
        """
        Filter entries based on search text.
        
        Filters the entry list to show only entries that contain
        the search text in their title, tags, or date information.
        
        Args:
            text (str): The search text to filter by
        """
        text = text.lower()
        # Filter entries based on case-insensitive text matching
        filtered = [(label, fname) for label, fname in self.all_entries if text in label.lower()]
        self.entry_list.clear()
        for label, _ in filtered:
            self.entry_list.addItem(label)

    def find_file_path(self, filename):
        """
        Find the full path of an entry file by searching the user's directory.
        
        Args:
            filename (str): The filename to search for
            
        Returns:
            str or None: The full path to the file, or None if not found
        """
        entry_dir = self.get_entry_dir()
        # Search recursively through user's entry directory
        for root, _, files in os.walk(entry_dir):
            if filename in files:
                return os.path.join(root, filename)
        return None

    def open_entry(self):
        """
        Open the selected entry in the editor window.
        
        Gets the currently selected entry from the list and opens
        it in a new EditorWindow instance for viewing and editing.
        """
        index = self.entry_list.currentRow()
        if index >= 0:
            # Get the filename from the selected entry
            _, file = self.all_entries[index]
            self.editor = EditorWindow(self.username, file)
            self.editor.show()
        else:
            QMessageBox.warning(self, "No Selection", "Please select an entry.")

    def new_entry(self):
        """
        Create a new journal entry.
        
        Opens a new EditorWindow instance for creating a new
        journal entry with the current theme settings.
        """
        self.editor = EditorWindow(self.username)
        self.editor.show()

    def delete_entry(self):
        """
        Delete the selected journal entry.
        
        Prompts the user for confirmation, then deletes both the
        encrypted entry file and its associated metadata file.
        Refreshes the entry list after deletion.
        """
        index = self.entry_list.currentRow()
        if index >= 0:
            label, file = self.all_entries[index]
            # Confirm deletion with user
            confirm = QMessageBox.question(self, "Confirm Delete", f"Delete entry:\n\n{label}?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                # Find and delete the entry file
                path = self.find_file_path(file)
                if path:
                    os.remove(path)
                    # Also delete the metadata file if it exists
                    meta_path = path.replace(".enc", ".meta.json")
                    if os.path.exists(meta_path):
                        os.remove(meta_path)
                    # Refresh the entry list
                    self.load_entries()
                else:
                    QMessageBox.warning(self, "Error", "Could not find the selected entry.")
        else:
            QMessageBox.warning(self, "No Selection", "Select an entry to delete.")

    def change_password(self):
        """
        Open the password change window.
        
        Creates and displays a new ChangePasswordWindow instance
        for the current user to change their account password.
        """
        from ui.change_password import ChangePasswordWindow
        self.change_window = ChangePasswordWindow(self.username)
        self.change_window.show()

    def logout(self):
        """
        Log out the current user and return to the login screen.
        
        Creates a new LoginWindow instance, displays it, and closes
        the current dashboard window to complete the logout process.
        """
        from ui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()