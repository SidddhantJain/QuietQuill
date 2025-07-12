"""
Entry Calendar Module

This module provides a calendar-based interface for viewing journal entries by date.
Users can see highlighted dates with entries and click on dates to view entry titles
for that specific day. Multiple entries per day are supported with a list dialog.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QMessageBox, QListWidget, QDialog, QDialogButtonBox
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QColor
import os, json

class EntryCalendarWindow(QWidget):
    """
    A calendar widget for displaying and accessing journal entries by date.
    
    This window provides a visual calendar interface where:
    - Dates with journal entries are highlighted in blue
    - Clicking on a date shows entry titles for that day
    - Single entries are displayed in a message box
    - Multiple entries are shown in a list dialog
    - Handles metadata parsing and file system operations
    
    Attributes:
        username (str): The username whose entries are being displayed
        entry_dir (str): Path to the directory containing user's entries
        calendar (QCalendarWidget): The main calendar widget for date selection
    """
    
    def __init__(self, username):
        """
        Initialize the EntryCalendarWindow for a specific user.
        
        Args:
            username (str): The username whose entries will be displayed on the calendar
        """
        super().__init__()
        self.username = username
        self.setWindowTitle("📆 Entry Calendar")
        self.setGeometry(500, 200, 400, 400)
        
        # Construct path to user's entries directory
        self.entry_dir = os.path.join("entries", username)
        
        # Initialize UI and apply entry date markings
        self.setup_ui()
        self.mark_entry_dates()

    def setup_ui(self):
        """
        Set up the user interface components for the calendar view.
        
        Creates and configures the calendar widget and connects it to the
        entry information display handler.
        """
        layout = QVBoxLayout()
        
        # Main calendar widget for date selection and display
        self.calendar = QCalendarWidget()
        # Connect calendar date clicks to entry information display
        self.calendar.clicked.connect(self.show_entry_info)
        layout.addWidget(self.calendar)
        
        self.setLayout(layout)

    def mark_entry_dates(self):
        """
        Mark calendar dates that have journal entries with visual highlighting.
        
        This method:
        1. Scans the user's entries directory for metadata files
        2. Extracts dates from entry metadata
        3. Applies blue background highlighting to dates with entries
        4. Handles file parsing errors gracefully
        """
        # Check if user has entries directory
        if not os.path.isdir(self.entry_dir):
            return
        
        # Set to store unique dates with entries (avoids duplicates)
        dates_with_entries = set()
        
        # Scan all metadata files in the entries directory
        for file in os.listdir(self.entry_dir):
            if file.endswith(".meta.json"):
                try:
                    # Parse metadata file to extract date information
                    with open(os.path.join(self.entry_dir, file)) as f:
                        meta = json.load(f)
                        date_str = meta.get("date")
                        if date_str:
                            dates_with_entries.add(date_str)
                except Exception:
                    # Skip corrupted or invalid metadata files
                    continue
        
        # Create text format for highlighting dates with entries
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#cce5ff"))  # Light blue background
        
        # Apply highlighting to each date with entries
        for date_str in dates_with_entries:
            try:
                # Convert date string to QDate object
                qdate = QDate.fromString(date_str, "yyyy-MM-dd")
                if qdate.isValid():
                    # Apply highlighting format to the calendar date
                    self.calendar.setDateTextFormat(qdate, fmt)
            except Exception:
                # Skip invalid date strings
                continue

    def show_entry_info(self, date: QDate):
        """
        Display entry information for a selected calendar date.
        
        This method handles clicking on calendar dates by:
        1. Finding all entries for the selected date
        2. Displaying single entries in a message box
        3. Showing multiple entries in a list dialog
        4. Providing feedback for dates with no entries
        
        Args:
            date (QDate): The calendar date that was clicked
        """
        # Convert QDate to string format for comparison
        date_str = date.toString("yyyy-MM-dd")
        entries = []
        
        # Check if user has entries directory
        if not os.path.isdir(self.entry_dir):
            QMessageBox.information(self, "No Entries", "No entries directory found for this user.")
            return
        
        # Search for entries matching the selected date
        for file in os.listdir(self.entry_dir):
            if file.endswith(".meta.json"):
                try:
                    # Parse metadata file to check date and extract title
                    with open(os.path.join(self.entry_dir, file)) as f:
                        meta = json.load(f)
                        if meta.get("date") == date_str:
                            # Use entry title or filename as fallback
                            entries.append(meta.get("title", file))
                except Exception:
                    # Skip corrupted or invalid metadata files
                    continue
        
        # Display entries based on count
        if entries:
            if len(entries) == 1:
                # Single entry - show in simple message box
                QMessageBox.information(self, "Entry", entries[0])
            else:
                # Multiple entries - show in list dialog
                self.show_entries_list(entries)
        else:
            # No entries found for this date
            QMessageBox.information(self, "No Entries", "No entries for this day.")

    def show_entries_list(self, entries):
        """
        Display a list of entry titles in a dialog window.
        
        This method creates a modal dialog with a list widget to display
        multiple entry titles when a date has more than one journal entry.
        
        Args:
            entries (list): List of entry titles to display
        """
        # Create modal dialog for displaying entry list
        dialog = QDialog(self)
        dialog.setWindowTitle("Entries")
        layout = QVBoxLayout(dialog)
        
        # List widget to display entry titles
        list_widget = QListWidget()
        list_widget.addItems(entries)
        layout.addWidget(list_widget)
        
        # OK button to close the dialog
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)
        
        # Show dialog as modal window
        dialog.exec_()
