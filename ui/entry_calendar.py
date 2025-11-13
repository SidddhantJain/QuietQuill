"""Entry calendar: highlight dates with entries and list titles for a selected day."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QMessageBox, QListWidget, QDialog, QDialogButtonBox
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QColor
import os, json

class EntryCalendarWindow(QWidget):
    """Calendar view: highlights dates with entries; shows titles on click."""
    
    def __init__(self, username):
        """Init with username; build UI and mark dates."""
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
        """Build calendar widget and connect click handler."""
        layout = QVBoxLayout()
        
        # Main calendar widget for date selection and display
        self.calendar = QCalendarWidget()
        # Connect calendar date clicks to entry information display
        self.calendar.clicked.connect(self.show_entry_info)
        layout.addWidget(self.calendar)
        
        self.setLayout(layout)

    def mark_entry_dates(self):
        """Scan entry metadata and highlight dates with entries."""
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
        """List entry titles for selected date (message box for one, dialog for many)."""
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
        """Modal dialog with a list of entry titles."""
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
