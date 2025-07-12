"""
Journal Entry Editor Module

This module provides a rich text editor for creating and editing journal entries
in the QuietQuill application. It supports features like image insertion, emoji
insertion, tagging, categorization, encryption, and basic sentiment analysis.
"""

import os
import json
import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QPushButton,
    QFileDialog, QMessageBox, QLabel, QHBoxLayout, QInputDialog,
    QComboBox, QLineEdit, QListWidget, QListWidgetItem, QDesktopWidget,
    QSpacerItem, QSizePolicy, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QTextImageFormat, QFont, QColor
from PyQt5.QtCore import Qt
from utils.encryption import encrypt_data, decrypt_data

class ImageDropTextEdit(QTextEdit):
    """
    A custom QTextEdit that supports drag-and-drop image insertion.
    
    This class extends QTextEdit to provide drag-and-drop functionality
    for image files. When an image is dropped onto the text area, it
    automatically inserts the image into the document with predefined
    dimensions.
    
    Supported image formats: PNG, JPG, JPEG, BMP, GIF
    """
    
    def __init__(self):
        """Initialize the ImageDropTextEdit with drag-and-drop enabled."""
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        """
        Handle drag enter events to accept file drops.
        
        Args:
            event: The drag enter event containing mime data
        """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        """
        Handle drop events to insert images into the text editor.
        
        Processes dropped files and inserts valid image files into the
        text editor with default dimensions (300x200 pixels).
        
        Args:
            event: The drop event containing file URLs
        """
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            # Check if dropped file is a valid image format
            if os.path.isfile(file_path) and file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                # Create image format with default dimensions
                img_format = QTextImageFormat()
                img_format.setName(file_path)
                img_format.setWidth(300)
                img_format.setHeight(200)
                self.textCursor().insertImage(img_format)
            else:
                super().dropEvent(event)

class EditorWindow(QWidget):
    """
    A comprehensive journal entry editor with rich text capabilities.
    
    This window provides a full-featured editor for creating and editing
    journal entries with the following features:
    - Rich text editing with HTML support
    - Image insertion via drag-and-drop or file dialog
    - Emoji insertion
    - Entry categorization and tagging
    - Encrypted storage with metadata
    - Basic sentiment analysis
    - Pin/unpin functionality
    - Responsive design with gradient styling
    - Tag suggestions based on existing entries
    
    Attributes:
        username (str): The username who owns the entry
        filename (str): The filename of the entry being edited (None for new entries)
        theme (str): The UI theme (currently unused)
        start_time (datetime): When the editing session started
        entry_dir (str): Directory path for storing user entries
        text_edit (ImageDropTextEdit): The main text editor widget
        title_label (QLabel): Display label for entry title
        category_combo (QComboBox): Dropdown for entry categorization
        tags_input (QLineEdit): Input field for entry tags
        suggestion_list (QListWidget): List of tag suggestions
    """
    
    def __init__(self, username, filename=None, theme="light"):
        """
        Initialize the EditorWindow for a specific user.
        
        Args:
            username (str): The username who owns the entry
            filename (str, optional): Filename of existing entry to edit
            theme (str, optional): UI theme preference (default: "light")
        """
        super().__init__()
        self.username = username
        self.filename = filename
        self.theme = theme
        
        # Record start time for metadata tracking
        self.start_time = datetime.datetime.now()
        
        # Ensure user's entry directory exists
        self.entry_dir = os.path.join("entries", self.username)
        os.makedirs(self.entry_dir, exist_ok=True)

        self.setWindowTitle("📝 QuietQuill - Editor")
        self.setMinimumSize(900, 600)
        self.setup_ui()

        # Load existing entry if filename provided
        if self.filename:
            self.load_entry()

        self.apply_dynamic_styles()

    def setup_ui(self):
        """
        Set up the user interface components and layout.
        
        Creates and configures all UI elements including:
        - Main layout with card-based design
        - Text editor with rich text capabilities
        - Category and tag input fields
        - Action buttons for various operations
        - Gradient styling and shadow effects
        """
        # Main layout setup with no margins for full-screen gradient effect
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Application title with emoji and styling
        self.title = QLabel("📖 <b>Diary Entry</b>")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("editorTitle")
        self.main_layout.addWidget(self.title, alignment=Qt.AlignHCenter)
        self.main_layout.addSpacing(8)

        # Card frame with gradient background and drop shadow for modern look
        self.card_frame = QFrame()
        self.card_frame.setObjectName("editorCard")
        # CSS-like styling for gradient background from cream to golden yellow
        self.card_frame.setStyleSheet("""
            QFrame#editorCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #fffbe7, stop:1 #ffe082);
                border-radius: 22px;
                padding: 36px 36px 28px 36px;
                margin: auto;
            }
        """)
        # Drop shadow effect for depth and modern appearance
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(255, 215, 64, 80))  # Semi-transparent golden shadow
        shadow.setOffset(0, 10)  # Slight vertical offset for depth
        self.card_frame.setGraphicsEffect(shadow)

        # Card layout for organizing editor components
        self.card_layout = QVBoxLayout(self.card_frame)
        self.card_layout.setSpacing(18)

        # Entry title display (shows filename without extension)
        self.title_label = QLabel("Untitled Entry")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 22px; color: #b28704; background: transparent;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.card_layout.addWidget(self.title_label)

        # Main text editor with drag-and-drop image support
        self.text_edit = ImageDropTextEdit()
        self.text_edit.setObjectName("diaryTextEdit")
        self.text_edit.setFont(QFont("Georgia", 16))  # Elegant serif font for writing
        self.card_layout.addWidget(self.text_edit)
        
        # Information label showing word count and mood analysis
        self.info_label = QLabel("Words: 0 | Mood: Neutral 😐")
        self.info_label.setAlignment(Qt.AlignRight)
        self.card_layout.addWidget(self.info_label)
        # Connect text changes to update word count and mood analysis
        self.text_edit.textChanged.connect(self.update_info_label)

        # Category selection dropdown
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Journal", "Dream", "Work", "Travel", "Other"])
        self.category_combo.setObjectName("categoryCombo")
        cat_row = QHBoxLayout()
        cat_row.addWidget(QLabel("Category:"))
        cat_row.addWidget(self.category_combo)
        self.card_layout.addLayout(cat_row)

        # Tags input field for entry organization
        tag_row = QHBoxLayout()
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Enter tags (comma-separated, e.g., dreams, travel)")
        self.tags_input.setObjectName("tagsInput")
        tag_row.addWidget(QLabel("Tags:"))
        tag_row.addWidget(self.tags_input)
        self.card_layout.addLayout(tag_row)

        # Tag suggestion list for easy tag selection
        self.suggestion_list = QListWidget()
        self.suggestion_list.setMaximumHeight(80)
        self.suggestion_list.setObjectName("suggestionList")
        self.suggestion_list.itemClicked.connect(self.insert_tag)
        self.card_layout.addWidget(QLabel("Suggestions:"))
        self.card_layout.addWidget(self.suggestion_list)

        # Action buttons row
        button_row = QHBoxLayout()
        button_row.setSpacing(14)

        # Create action buttons with icons and labels
        emoji_btn = QPushButton("😊\nEmoji")
        emoji_btn.clicked.connect(self.insert_emoji)
        img_btn = QPushButton("🖼️\nImage")
        img_btn.clicked.connect(self.insert_image)
        self.pin_btn = QPushButton("📌\nPin/Unpin")
        self.pin_btn.clicked.connect(self.toggle_pin)
        save_btn = QPushButton("💾\nSave")
        save_btn.clicked.connect(self.save_entry)

        # Apply consistent styling to all buttons
        for btn in [emoji_btn, img_btn, self.pin_btn, save_btn]:
            btn.setMinimumHeight(60)
            btn.setMaximumHeight(70)
            btn.setMinimumWidth(90)
            btn.setMaximumWidth(110)
            btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 15px;
                    font-weight: bold;
                    padding: 8px 6px;
                    border-radius: 14px;
                    background-color: #ffd54f;
                    color: #795548;
                    border: none;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #ffe082;
                }
            """)
            button_row.addWidget(btn)

        self.card_layout.addLayout(button_row)
        self.main_layout.addWidget(self.card_frame, alignment=Qt.AlignHCenter)
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.main_layout)

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
        
        This method calculates scaling factors and applies appropriate
        styling to all UI components to maintain visual consistency
        across different screen sizes.
        """
        # Calculate scaling based on window dimensions
        w = max(self.width(), 900)
        h = max(self.height(), 600)
        scale = min(w / 1200, h / 800)
        scale = max(0.7, min(scale, 1.5))  # Clamp scale between 0.7 and 1.5

        # Define color scheme for consistent theming
        card_grad = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fffbe7, stop:1 #ffe082)"
        title_color = "#b28704"
        label_color = "#795548"
        input_bg = "#fffde7"
        input_border = "#ffd54f"
        input_text = "#795548"
        list_bg = "#fffde7"
        list_border = "#ffd54f"

        # Apply base background color
        self.setStyleSheet(f"background: #fffde7;")
        self.card_frame.setMaximumWidth(int(self.width() * 0.98))
        
        # Scale and style various UI components
        self.title.setStyleSheet(f"""
            font-size: 36px;
            font-weight: bold;
            color: {title_color};
            margin-bottom: {int(8 * scale)}px;
            background: transparent;
        """)
        self.title_label.setStyleSheet(f"""
            font-size: 22px;
            font-weight: bold;
            color: {title_color};
            background: transparent;
        """)
        self.text_edit.setStyleSheet(f"""
            QTextEdit {{
                background: {input_bg};
                color: {input_text};
                border: 2px solid {input_border};
                border-radius: 14px;
                font-family: 'Georgia', 'Times New Roman', serif;
                font-size: 17px;
                padding: 14px;
            }}
        """)
        self.info_label.setStyleSheet(f"""
            font-size: 14px;
            color: {label_color};
            background: transparent;
        """)
        self.category_combo.setStyleSheet(f"""
            QComboBox {{
                background: {input_bg};
                color: {input_text};
                border: 2px solid {input_border};
                border-radius: 8px;
                font-size: 15px;
                padding: 6px;
            }}
        """)
        self.tags_input.setStyleSheet(f"""
            QLineEdit {{
                background: {input_bg};
                color: {input_text};
                border: 2px solid {input_border};
                border-radius: 8px;
                font-size: 15px;
                padding: 6px;
            }}
        """)
        self.suggestion_list.setStyleSheet(f"""
            QListWidget {{
                background: {list_bg};
                border: 2px solid {list_border};
                border-radius: 8px;
                font-size: 14px;
                color: {input_text};
                padding: 4px;
            }}
        """)
        self.card_frame.setStyleSheet(f"""
            QFrame#editorCard {{
                background: {card_grad};
                border-radius: 22px;
                padding: 36px 36px 28px 36px;
                margin: auto;
            }}
        """)

    def load_entry(self):
        """
        Load an existing entry from encrypted storage.
        
        Decrypts the entry content and loads associated metadata including
        tags, category, and other entry properties. Updates the UI to
        display the loaded content.
        """
        enc_path = self.get_full_entry_path(self.filename)
        try:
            # Decrypt and load entry content
            content = decrypt_data(enc_path)
            self.text_edit.setHtml(content)
            self.title_label.setText(self.filename.replace(".enc", ""))

            # Load metadata if available
            meta_path = enc_path.replace(".enc", ".meta.json")
            if os.path.exists(meta_path):
                with open(meta_path, "r") as f:
                    meta = json.load(f)
                    # Restore tags if present
                    if "tags" in meta:
                        self.tags_input.setText(", ".join(meta["tags"]))
                    # Restore category selection if present
                    if "category" in meta:
                        idx = self.category_combo.findText(meta["category"])
                        if idx != -1:
                            self.category_combo.setCurrentIndex(idx)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load entry: {str(e)}")

    def insert_emoji(self):
        """
        Insert an emoji into the text editor at the current cursor position.
        
        Prompts the user to enter an emoji and inserts it into the text
        editor at the current cursor location.
        """
        emoji, ok = QInputDialog.getText(self, "Insert Emoji", "Enter Emoji (😊, 😢, ❤️ etc.):")
        if ok and emoji:
            cursor = self.text_edit.textCursor()
            cursor.insertText(emoji)

    def insert_image(self):
        """
        Insert an image into the text editor with user-specified dimensions.
        
        Opens a file dialog to select an image, prompts for dimensions,
        and inserts the image into the text editor at the current cursor position.
        """
        # Open file dialog to select image
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            # Get image dimensions from user
            width, ok1 = QInputDialog.getInt(self, "Image Width", "Width (px):", 200, 50, 800)
            if ok1:
                height, ok2 = QInputDialog.getInt(self, "Image Height", "Height (px):", 200, 50, 800)
                if ok2:
                    # Create and insert image with specified dimensions
                    img_format = QTextImageFormat()
                    img_format.setName(file_path)
                    img_format.setWidth(width)
                    img_format.setHeight(height)
                    cursor = self.text_edit.textCursor()
                    cursor.insertImage(img_format)

    def save_entry(self):
        """
        Save the current entry to encrypted storage with metadata.
        
        This method performs the following operations:
        1. Gets the HTML content from the text editor
        2. Prompts for title if this is a new entry
        3. Creates directory structure based on date
        4. Encrypts and saves the entry content
        5. Saves metadata including tags, category, and timestamps
        6. Provides user feedback and closes the editor
        """
        content = self.text_edit.toHtml()

        # Handle new entry title input
        if not self.filename:
            title, ok = QInputDialog.getText(self, "Save Entry", "Enter title:")
            if not ok or not title.strip():
                QMessageBox.warning(self, "Error", "Entry title is required.")
                return
            # Generate filename with timestamp and title
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
            self.filename = f"{timestamp}_{title.strip().replace(' ', '_')}.enc"

        # Create directory structure by year/month for organization
        year = self.start_time.strftime("%Y")
        month = self.start_time.strftime("%m")
        save_dir = os.path.join(self.entry_dir, year, month)
        os.makedirs(save_dir, exist_ok=True)
        enc_path = os.path.join(save_dir, self.filename)

        # Encrypt and save entry content
        try:
            encrypt_data(content, enc_path, self.username)
        except TypeError:
            # Backward compatibility for older encryption function signature
            encrypt_data(content, enc_path)
        except Exception as e:
            QMessageBox.critical(self, "Encryption Error", f"Failed to encrypt entry: {str(e)}")
            return

        # Prepare and save metadata
        tags = [t.strip() for t in self.tags_input.text().split(",") if t.strip()]
        category = self.category_combo.currentText()
        meta = {
            "username": self.username,
            "filename": self.filename,
            "title": self.filename.replace(".enc", ""),
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tags": tags,
            "category": category
        }
        meta_path = enc_path.replace(".enc", ".meta.json")
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)

        QMessageBox.information(self, "Saved", "Entry saved successfully.")
        self.close()

    def get_full_entry_path(self, filename):
        """
        Find the full path of an entry file by searching the user's directory.
        
        Args:
            filename (str): The filename to search for
            
        Returns:
            str: The full path to the file
            
        Raises:
            FileNotFoundError: If the file is not found in any subdirectory
        """
        # Search recursively through user's entry directory
        for root, _, files in os.walk(self.entry_dir):
            if filename in files:
                return os.path.join(root, filename)
        raise FileNotFoundError(f"File '{filename}' not found.")
    
    def update_info_label(self):
        """
        Update the information label with word count and mood analysis.
        
        This method performs basic sentiment analysis by counting positive
        and negative words in the text and displays the result along with
        the word count.
        """
        text = self.text_edit.toPlainText()
        word_count = len(text.strip().split())

        # Simple sentiment analysis using predefined word lists
        happy_words = {"happy", "joy", "excited", "love", "grateful", "awesome", "smile"}
        sad_words = {"sad", "tired", "angry", "depressed", "cry", "lonely", "hate"}

        # Calculate sentiment score
        score = 0
        for word in text.lower().split():
            if word in happy_words:
                score += 1
            elif word in sad_words:
                score -= 1

        # Determine mood based on sentiment score
        if score > 0:
            mood = "Happy 😊"
        elif score < 0:
            mood = "Sad 😢"
        else:
            mood = "Neutral 😐"

        self.info_label.setText(f"Words: {word_count} | Mood: {mood}")

    def populate_tag_suggestions(self):
        """
        Populate the tag suggestions list with tags from existing entries.
        
        Scans all existing entries to collect unique tags and displays
        them in the suggestions list for easy selection.
        """
        tag_set = set()
        # Search through all metadata files to collect tags
        for root, _, files in os.walk(self.entry_dir):
            for file in files:
                if file.endswith(".meta.json"):
                    try:
                        with open(os.path.join(root, file), "r") as f:
                            meta = json.load(f)
                            tags = meta.get("tags", [])
                            for tag in tags:
                                tag_set.add(tag)
                    except:
                        # Skip corrupted metadata files
                        continue
        
        # Populate suggestions list with sorted unique tags
        self.suggestion_list.clear()
        for tag in sorted(tag_set):
            item = QListWidgetItem(tag)
            self.suggestion_list.addItem(item)

    def insert_tag(self, item):
        """
        Insert a selected tag from the suggestions list into the tags input.
        
        Args:
            item (QListWidgetItem): The selected tag item from the suggestions list
        """
        tag = item.text()
        current_tags = self.tags_input.text()
        tag_list = [t.strip() for t in current_tags.split(",") if t.strip()]
        
        # Add tag only if not already present
        if tag not in tag_list:
            tag_list.append(tag)
            self.tags_input.setText(", ".join(tag_list))

    def toggle_pin(self):
        """
        Toggle the pin status of the currently selected entry.
        
        This method updates the metadata to mark an entry as pinned or unpinned,
        which affects its display order in entry lists.
        """
        selected = self.entry_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "No Entry", "Select an entry to pin/unpin.")
            return

        # Get entry path and metadata
        enc_path = selected.data(Qt.UserRole)
        meta_path = enc_path.replace(".enc", ".meta.json")

        if os.path.exists(meta_path):
            # Load existing metadata
            with open(meta_path, "r") as f:
                meta = json.load(f)

            # Toggle pin status
            meta["pinned"] = not meta.get("pinned", False)

            # Save updated metadata
            with open(meta_path, "w") as f:
                json.dump(meta, f, indent=2)

            QMessageBox.information(self, "Updated", f"{'Pinned' if meta['pinned'] else 'Unpinned'} successfully.")
            self.load_entries()
    
    def load_entries(self):
        """
        Load and display all entries for the current user.
        
        Scans the user's entry directory and populates the entry list
        with entries, showing pinned entries first followed by others
        in alphabetical order.
        """
        self.entry_list.clear()
        entries = []

        # Collect all entries with their metadata
        for root, _, files in os.walk(os.path.join("entries", self.username)):
            for file in files:
                if file.endswith(".enc"):
                    enc_path = os.path.join(root, file)
                    meta_path = enc_path.replace(".enc", ".meta.json")
                    pinned = False
                    title = file.replace(".enc", "")
                    
                    # Load metadata if available
                    if os.path.exists(meta_path):
                        with open(meta_path, "r") as f:
                            meta = json.load(f)
                            title = meta.get("title", title)
                            pinned = meta.get("pinned", False)
                    entries.append((pinned, title, enc_path))

        # Sort entries: pinned first, then alphabetically
        entries.sort(key=lambda x: (not x[0], x[1].lower()))

        # Add entries to the list widget
        for pinned, title, path in entries:
            display_text = f"📌 {title}" if pinned else title
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, path)
            self.entry_list.addItem(item)


