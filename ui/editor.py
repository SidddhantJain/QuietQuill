import os
import json
import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QPushButton,
    QFileDialog, QMessageBox, QLabel, QHBoxLayout, QInputDialog,
    QComboBox, QLineEdit, QListWidget, QListWidgetItem, QDesktopWidget
)
from PyQt5.QtGui import QTextImageFormat
from PyQt5.QtCore import Qt
from utils.encryption import encrypt_data, decrypt_data
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextImageFormat
from PyQt5.QtCore import QUrl

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextImageFormat
from PyQt5.QtCore import QUrl
import os

class ImageDropTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path) and file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                img_format = QTextImageFormat()
                img_format.setName(file_path)
                img_format.setWidth(300)  # default size
                img_format.setHeight(200)
                self.textCursor().insertImage(img_format)
            else:
                super().dropEvent(event)


class EditorWindow(QWidget):
    def __init__(self, username, filename=None, theme="light"):
        super().__init__()
        self.username = username
        self.filename = filename
        self.theme = theme
        self.start_time = datetime.datetime.now()
        self.entry_dir = os.path.join("entries", self.username)
        os.makedirs(self.entry_dir, exist_ok=True)

        self.setWindowTitle("📝 QuietQuill - Editor")

        # Set window size to 80% of the screen
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.8)
        height = int(screen.height() * 0.8)
        self.setGeometry(
            (screen.width() - width) // 2,
            (screen.height() - height) // 2,
            width,
            height
        )

        self.setup_ui()
        

        if self.filename:
            self.load_entry()

        # Apply selected theme
        self.apply_theme(self.theme)

    def apply_theme(self, mode):
        if mode == "dark":
            dark_stylesheet = """
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-family: Segoe UI;
            }
            QLineEdit, QTextEdit, QListWidget {
                background-color: #2c2c2c;
                color: #ffffff;
                border: 1px solid #444;
            }
            QPushButton {
                background-color: #444;
                color: white;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            """
            self.setStyleSheet(dark_stylesheet)
        else:
            self.setStyleSheet("")  # Default light style


    def setup_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Untitled Entry")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(self.title_label)

        self.text_edit = ImageDropTextEdit()
        layout.addWidget(self.text_edit)
        self.info_label = QLabel("Words: 0 | Mood: Neutral 😐")
        layout.addWidget(self.info_label)
        self.text_edit.textChanged.connect(self.update_info_label)

        # Category Dropdown
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Journal", "Dream", "Work", "Travel", "Other"])
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(self.category_combo)

        # Tags
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Enter tags (comma-separated, e.g., dreams, travel)")
        layout.addWidget(QLabel("Tags:"))
        layout.addWidget(self.tags_input)

        # Tag Suggestion List
        self.suggestion_list = QListWidget()
        self.suggestion_list.setMaximumHeight(80)
        self.suggestion_list.itemClicked.connect(self.insert_tag)
        layout.addWidget(QLabel("Suggestions:"))
        layout.addWidget(self.suggestion_list)

        # Button Row
        button_row = QHBoxLayout()

        emoji_btn = QPushButton("😊 Insert Emoji")
        emoji_btn.clicked.connect(self.insert_emoji)

        img_btn = QPushButton("🖼️ Insert Image")
        img_btn.clicked.connect(self.insert_image)

        self.pin_btn = QPushButton("📌 Pin/Unpin Entry")
        self.pin_btn.clicked.connect(self.toggle_pin)
        layout.addWidget(self.pin_btn)  # Changed from self.layout to layout

        save_btn = QPushButton("💾 Save Entry")
        save_btn.clicked.connect(self.save_entry)

        button_row.addWidget(emoji_btn)
        button_row.addWidget(img_btn)
        button_row.addWidget(save_btn)

        layout.addLayout(button_row)
        self.setLayout(layout)

    def load_entry(self):
        enc_path = self.get_full_entry_path(self.filename)
        try:
            content = decrypt_data(enc_path)
            self.text_edit.setHtml(content)
            self.title_label.setText(self.filename.replace(".enc", ""))

            # Load tags and category
            meta_path = enc_path.replace(".enc", ".meta.json")
            if os.path.exists(meta_path):
                with open(meta_path, "r") as f:
                    meta = json.load(f)
                    if "tags" in meta:
                        self.tags_input.setText(", ".join(meta["tags"]))
                    if "category" in meta:
                        idx = self.category_combo.findText(meta["category"])
                        if idx != -1:
                            self.category_combo.setCurrentIndex(idx)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load entry: {str(e)}")

    def insert_emoji(self):
        emoji, ok = QInputDialog.getText(self, "Insert Emoji", "Enter Emoji (😊, 😢, ❤️ etc.):")
        if ok and emoji:
            cursor = self.text_edit.textCursor()
            cursor.insertText(emoji)

    def insert_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            width, ok1 = QInputDialog.getInt(self, "Image Width", "Width (px):", 200, 50, 800)
            if ok1:
                height, ok2 = QInputDialog.getInt(self, "Image Height", "Height (px):", 200, 50, 800)
                if ok2:
                    img_format = QTextImageFormat()
                    img_format.setName(file_path)
                    img_format.setWidth(width)
                    img_format.setHeight(height)
                    cursor = self.text_edit.textCursor()
                    cursor.insertImage(img_format)

    def save_entry(self):
        content = self.text_edit.toHtml()

        if not self.filename:
            title, ok = QInputDialog.getText(self, "Save Entry", "Enter title:")
            if not ok or not title.strip():
                QMessageBox.warning(self, "Error", "Entry title is required.")
                return
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
            self.filename = f"{timestamp}_{title.strip().replace(' ', '_')}.enc"

        year = self.start_time.strftime("%Y")
        month = self.start_time.strftime("%m")
        save_dir = os.path.join(self.entry_dir, year, month)
        os.makedirs(save_dir, exist_ok=True)
        enc_path = os.path.join(save_dir, self.filename)
        encrypt_data(content, enc_path)

        # Save meta
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
        for root, _, files in os.walk(self.entry_dir):
            if filename in files:
                return os.path.join(root, filename)
        raise FileNotFoundError(f"File '{filename}' not found.")
    
    def update_info_label(self):
        text = self.text_edit.toPlainText()
        word_count = len(text.strip().split())

        # Basic sentiment analysis using keyword matching
        happy_words = {"happy", "joy", "excited", "love", "grateful", "awesome", "smile"}
        sad_words = {"sad", "tired", "angry", "depressed", "cry", "lonely", "hate"}

        score = 0
        for word in text.lower().split():
            if word in happy_words:
                score += 1
            elif word in sad_words:
                score -= 1

        if score > 0:
            mood = "Happy 😊"
        elif score < 0:
            mood = "Sad 😢"
        else:
            mood = "Neutral 😐"

        self.info_label.setText(f"Words: {word_count} | Mood: {mood}")


    def populate_tag_suggestions(self):
        tag_set = set()
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
                        continue
        self.suggestion_list.clear()
        for tag in sorted(tag_set):
            item = QListWidgetItem(tag)
            self.suggestion_list.addItem(item)

    def insert_tag(self, item):
        tag = item.text()
        current_tags = self.tags_input.text()
        tag_list = [t.strip() for t in current_tags.split(",") if t.strip()]
        if tag not in tag_list:
            tag_list.append(tag)
            self.tags_input.setText(", ".join(tag_list))

    def toggle_pin(self):
        selected = self.entry_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "No Entry", "Select an entry to pin/unpin.")
            return

        enc_path = selected.data(Qt.UserRole)
        meta_path = enc_path.replace(".enc", ".meta.json")

        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                meta = json.load(f)

            meta["pinned"] = not meta.get("pinned", False)

            with open(meta_path, "w") as f:
                json.dump(meta, f, indent=2)

            QMessageBox.information(self, "Updated", f"{'Pinned' if meta['pinned'] else 'Unpinned'} successfully.")
            self.load_entries()
    
    def load_entries(self):
        self.entry_list.clear()
        entries = []

        for root, _, files in os.walk(os.path.join("entries", self.username)):
            for file in files:
                if file.endswith(".enc"):
                    enc_path = os.path.join(root, file)
                    meta_path = enc_path.replace(".enc", ".meta.json")
                    pinned = False
                    title = file.replace(".enc", "")
                    if os.path.exists(meta_path):
                        with open(meta_path, "r") as f:
                            meta = json.load(f)
                            title = meta.get("title", title)
                            pinned = meta.get("pinned", False)
                    entries.append((pinned, title, enc_path))

        # Pinned first, then others
        entries.sort(key=lambda x: (not x[0], x[1].lower()))

        for pinned, title, path in entries:
            display_text = f"📌 {title}" if pinned else title
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, path)
            self.entry_list.addItem(item)


