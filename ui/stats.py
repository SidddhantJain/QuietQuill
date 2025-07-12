"""
Statistics Window Module

This module provides a statistics window that displays various metrics about
a user's journal entries, including total entries, word counts, and activity patterns.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
import os, json

class StatsWindow(QWidget):
    """
    A PyQt5 widget that displays statistical information about user's journal entries.
    
    This window analyzes metadata files to provide insights such as:
    - Total number of entries
    - Longest entry by word count
    - Average words per entry
    - Most active writing day
    - Date range of entries (earliest to latest)
    
    Attributes:
        username (str): The username whose statistics are being displayed
        entry_dir (str): Path to the directory containing user's entries
    """
    
    def __init__(self, username):
        """
        Initialize the StatsWindow with a specific username.
        
        Args:
            username (str): The username whose statistics will be displayed
        """
        super().__init__()
        self.username = username
        self.setWindowTitle("📊 Entry Statistics")
        self.setGeometry(550, 250, 350, 250)
        
        # Construct path to user's entries directory
        self.entry_dir = os.path.join("entries", username)
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface and calculate statistics from entry metadata.
        
        This method:
        1. Scans the user's entries directory for metadata files
        2. Calculates various statistics from the metadata
        3. Creates and displays labels with the calculated statistics
        """
        layout = QVBoxLayout()
        
        # Initialize statistics variables
        total_entries = 0
        longest_entry = 0  # Word count of the longest entry
        wordiest_title = ""  # Title of the entry with most words
        date_count = {}  # Dictionary to track entries per date
        total_words = 0  # Sum of all words across all entries
        dates = []  # List of all entry dates for range calculation

        # Check if user has any entries
        if not os.path.isdir(self.entry_dir):
            layout.addWidget(QLabel("No entries found for this user."))
            self.setLayout(layout)
            return

        # Process each metadata file in the entries directory
        for file in os.listdir(self.entry_dir):
            if file.endswith(".meta.json"):
                try:
                    total_entries += 1
                    meta_path = os.path.join(self.entry_dir, file)
                    
                    # Load and parse metadata file
                    with open(meta_path) as f:
                        meta = json.load(f)
                    
                    # Extract word count and update totals
                    word_count = meta.get("word_count", 0)
                    total_words += word_count
                    
                    # Track the entry with most words
                    if word_count > longest_entry:
                        longest_entry = word_count
                        wordiest_title = meta.get("title", "")
                    
                    # Count entries per date for activity analysis
                    date = meta.get("date", "")
                    if date:
                        date_count[date] = date_count.get(date, 0) + 1
                        dates.append(date)
                        
                except Exception:
                    # Skip corrupted or invalid metadata files
                    continue

        # Calculate derived statistics
        # Find the date with most entries
        most_active_day = max(date_count.items(), key=lambda x: x[1], default=("N/A", 0))
        
        # Calculate average words per entry (integer division to avoid decimals)
        avg_words = total_words // total_entries if total_entries else 0
        
        # Find date range of entries
        earliest = min(dates) if dates else "N/A"
        latest = max(dates) if dates else "N/A"

        # Create and add statistic labels to the layout
        layout.addWidget(QLabel(f"📝 Total Entries: {total_entries}"))
        layout.addWidget(QLabel(f"📚 Longest Entry: {wordiest_title} ({longest_entry} words)"))
        layout.addWidget(QLabel(f"✍️ Average Words per Entry: {avg_words}"))
        layout.addWidget(QLabel(f"📆 Most Active Day: {most_active_day[0]} ({most_active_day[1]} entries)"))
        layout.addWidget(QLabel(f"⏳ Earliest Entry: {earliest}"))
        layout.addWidget(QLabel(f"🕰️ Latest Entry: {latest}"))
        
        # Apply the layout to the widget
        self.setLayout(layout)
