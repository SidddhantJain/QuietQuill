"""
Mood Tracker Module

This module provides a calendar-based mood tracking system for the QuietQuill application.
Users can select dates on a calendar and assign emoji moods to track their emotional state
over time. The mood data is persisted in JSON format for each user.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QInputDialog, QMessageBox, QDialog, QGridLayout, QPushButton
import os, json
from PyQt5.QtCore import QDate

class EmojiPickerDialog(QDialog):
    """
    A dialog window for selecting emoji moods.
    
    This dialog presents a grid of emoji buttons that users can click to select
    their mood for a specific date. The selected emoji is stored and returned
    to the calling mood tracker window.
    
    Attributes:
        selected_emoji (str): The emoji selected by the user, None if no selection
    """
    
    def __init__(self):
        """
        Initialize the EmojiPickerDialog with default settings.
        
        Sets up the dialog window properties and initializes the emoji selection UI.
        """
        super().__init__()
        self.setWindowTitle("Select Emoji")
        self.setGeometry(300, 300, 300, 200)
        self.selected_emoji = None  # Track which emoji was selected
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface for emoji selection.
        
        Creates a grid layout with emoji buttons arranged in a 5x2 grid pattern.
        Each button displays an emoji and connects to the selection handler.
        """
        layout = QGridLayout()
        
        # Predefined set of common mood emojis
        emojis = ["😊", "😔", "😎", "😡", "🥳", "😂", "❤️", "👍", "🎉", "🙌"]
        
        # Create buttons for each emoji and arrange in grid
        for i, emoji in enumerate(emojis):
            btn = QPushButton(emoji)
            btn.setStyleSheet("font-size: 24px;")  # Large font for better visibility
            # Lambda with default parameter to capture emoji value correctly
            btn.clicked.connect(lambda _, e=emoji: self.select_emoji(e))
            # Calculate grid position: 5 columns, multiple rows
            layout.addWidget(btn, i // 5, i % 5)
        
        self.setLayout(layout)

    def select_emoji(self, emoji):
        """
        Handle emoji selection and close the dialog.
        
        Args:
            emoji (str): The emoji that was selected by the user
        """
        self.selected_emoji = emoji
        self.accept()  # Close dialog with accepted status

class MoodTrackerWindow(QWidget):
    """
    A calendar-based mood tracking window for journal users.
    
    This window provides a calendar interface where users can:
    - Click on dates to set mood for that day
    - View previously set moods as calendar markings
    - Persist mood data in JSON format
    - Track emotional patterns over time
    
    Attributes:
        username (str): The username whose moods are being tracked
        mood_file (str): Path to the JSON file storing mood data
        mood_data (dict): Dictionary mapping date strings to emoji moods
        calendar (QCalendarWidget): The main calendar widget for date selection
    """
    
    def __init__(self, username):
        """
        Initialize the MoodTrackerWindow for a specific user.
        
        Args:
            username (str): The username whose moods will be tracked
        """
        super().__init__()
        self.username = username
        self.setWindowTitle("📅 Mood Tracker")
        self.setGeometry(400, 200, 400, 400)
        
        # Construct path to user's mood data file
        self.mood_file = os.path.join("entries", self.username, "moods.json")
        
        # Load existing mood data or initialize empty dictionary
        self.mood_data = self.load_mood_data()
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface components for mood tracking.
        
        Creates and configures the calendar widget and connects it to the
        mood selection handler. Also applies any existing mood markings.
        """
        layout = QVBoxLayout()

        # Main calendar widget for date selection
        self.calendar = QCalendarWidget()
        # Connect calendar clicks to mood setting functionality
        self.calendar.clicked.connect(self.set_mood_for_day)
        layout.addWidget(self.calendar)

        self.setLayout(layout)
        # Apply visual indicators for dates with existing mood data
        self.update_calendar_marks()

    def load_mood_data(self):
        """
        Load mood data from the user's JSON file.
        
        Returns:
            dict: Dictionary mapping date strings (YYYY-MM-DD) to emoji moods,
                  or empty dict if file doesn't exist or is invalid
        """
        if os.path.exists(self.mood_file):
            try:
                with open(self.mood_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # Return empty dict if file is corrupted or unreadable
                return {}
        return {}

    def set_mood_for_day(self, date: QDate):
        """
        Handle mood setting for a selected calendar date.
        
        Opens an emoji picker dialog and saves the selected mood for the
        specified date. Updates the calendar display and persists data.
        
        Args:
            date (QDate): The calendar date that was clicked
        """
        # Convert QDate to string format for storage
        selected_date = date.toString("yyyy-MM-dd")
        
        # Show emoji picker dialog
        emoji_picker = EmojiPickerDialog()
        
        # Process mood selection if user made a choice
        if emoji_picker.exec_() == QDialog.Accepted and emoji_picker.selected_emoji:
            mood = emoji_picker.selected_emoji
            
            # Update mood data for the selected date
            self.mood_data[selected_date] = mood
            
            # Persist mood data to JSON file
            try:
                with open(self.mood_file, "w") as f:
                    json.dump(self.mood_data, f, indent=2)
                
                # Provide user feedback
                QMessageBox.information(self, "Mood Saved", f"Mood for {selected_date}: {mood}")
                
                # Update calendar visual indicators
                self.update_calendar_marks()
                
            except IOError:
                # Handle file writing errors
                QMessageBox.warning(self, "Error", "Failed to save mood data.")

    def update_calendar_marks(self):
        """
        Update calendar visual indicators to show dates with mood data.
        
        This method applies formatting to calendar dates that have associated
        mood data, making it easy for users to see which dates have been
        tracked. Currently uses tooltips to display the mood emoji.
        """
        # Reset formatting to default for current date
        fmt = self.calendar.dateTextFormat(QDate.currentDate())
        fmt.setFontWeight(0)

        # Apply mood indicators to dates with mood data
        for date_str, emoji in self.mood_data.items():
            try:
                # Convert date string back to QDate object
                date = QDate.fromString(date_str, "yyyy-MM-dd")
                
                # Get current format for this date
                fmt = self.calendar.dateTextFormat(date)
                
                # Add emoji as tooltip (hover text)
                fmt.setToolTip(emoji)
                
                # Apply the updated format to the calendar
                self.calendar.setDateTextFormat(date, fmt)
                
            except Exception:
                # Skip invalid date entries
                continue
