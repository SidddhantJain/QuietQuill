"""Mood tracker: calendar to set emoji moods; persists per-user JSON data."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QInputDialog, QMessageBox, QDialog, QGridLayout, QPushButton
import os, json
from PyQt5.QtCore import QDate

class EmojiPickerDialog(QDialog):
    """Emoji picker dialog with a simple grid of buttons; returns selected emoji."""
    
    def __init__(self):
        """Init dialog UI and emoji grid."""
        super().__init__()
        self.setWindowTitle("Select Emoji")
        self.setGeometry(300, 300, 300, 200)
        self.selected_emoji = None  # Track which emoji was selected
        self.setup_ui()

    def setup_ui(self):
        """Build emoji grid (5x2) and connect clicks."""
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
        """Set selected emoji and accept dialog."""
        self.selected_emoji = emoji
        self.accept()  # Close dialog with accepted status

class MoodTrackerWindow(QWidget):
    """Calendar-based mood tracker for a user; stores date→emoji in JSON."""
    
    def __init__(self, username):
        """Init for username and load mood data."""
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
        """Build calendar, connect click handler, and apply markings."""
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
        """Load mood JSON for user; return dict or {} on error/missing."""
        if os.path.exists(self.mood_file):
            try:
                with open(self.mood_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # Return empty dict if file is corrupted or unreadable
                return {}
        return {}

    def set_mood_for_day(self, date: QDate):
        """Pick emoji for selected date, save to JSON, refresh indicators."""
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
        """Apply tooltip indicators to dates with saved moods."""
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
