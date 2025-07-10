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
                img_format.setWidth(300)
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
        self.setMinimumSize(900, 600)
        self.setup_ui()

        if self.filename:
            self.load_entry()

        self.apply_dynamic_styles()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Title above the card
        self.title = QLabel("📖 <b>Diary Entry</b>")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("editorTitle")
        self.main_layout.addWidget(self.title, alignment=Qt.AlignHCenter)
        self.main_layout.addSpacing(8)

        # Card frame with gradient and shadow
        self.card_frame = QFrame()
        self.card_frame.setObjectName("editorCard")
        self.card_frame.setStyleSheet("""
            QFrame#editorCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #fffbe7, stop:1 #ffe082);
                border-radius: 22px;
                padding: 36px 36px 28px 36px;
                margin: auto;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(255, 215, 64, 80))
        shadow.setOffset(0, 10)
        self.card_frame.setGraphicsEffect(shadow)

        self.card_layout = QVBoxLayout(self.card_frame)
        self.card_layout.setSpacing(18)

        # Entry title label (editable)
        self.title_label = QLabel("Untitled Entry")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 22px; color: #b28704; background: transparent;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.card_layout.addWidget(self.title_label)

        # Diary text area
        self.text_edit = ImageDropTextEdit()
        self.text_edit.setObjectName("diaryTextEdit")
        self.text_edit.setFont(QFont("Georgia", 16))
        self.card_layout.addWidget(self.text_edit)
        self.info_label = QLabel("Words: 0 | Mood: Neutral 😐")
        self.info_label.setAlignment(Qt.AlignRight)
        self.card_layout.addWidget(self.info_label)
        self.text_edit.textChanged.connect(self.update_info_label)

        # Category Dropdown
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Journal", "Dream", "Work", "Travel", "Other"])
        self.category_combo.setObjectName("categoryCombo")
        cat_row = QHBoxLayout()
        cat_row.addWidget(QLabel("Category:"))
        cat_row.addWidget(self.category_combo)
        self.card_layout.addLayout(cat_row)

        # Tags
        tag_row = QHBoxLayout()
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Enter tags (comma-separated, e.g., dreams, travel)")
        self.tags_input.setObjectName("tagsInput")
        tag_row.addWidget(QLabel("Tags:"))
        tag_row.addWidget(self.tags_input)
        self.card_layout.addLayout(tag_row)

        # Tag Suggestion List
        self.suggestion_list = QListWidget()
        self.suggestion_list.setMaximumHeight(80)
        self.suggestion_list.setObjectName("suggestionList")
        self.suggestion_list.itemClicked.connect(self.insert_tag)
        self.card_layout.addWidget(QLabel("Suggestions:"))
        self.card_layout.addWidget(self.suggestion_list)

        # Button Row
        button_row = QHBoxLayout()
        button_row.setSpacing(14)

        emoji_btn = QPushButton("😊\nEmoji")
        emoji_btn.clicked.connect(self.insert_emoji)
        img_btn = QPushButton("🖼️\nImage")
        img_btn.clicked.connect(self.insert_image)
        self.pin_btn = QPushButton("📌\nPin/Unpin")
        self.pin_btn.clicked.connect(self.toggle_pin)
        save_btn = QPushButton("💾\nSave")
        save_btn.clicked.connect(self.save_entry)

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
        self.apply_dynamic_styles()
        return super().resizeEvent(event)

    def apply_dynamic_styles(self):
        w = max(self.width(), 900)
        h = max(self.height(), 600)
        scale = min(w / 1200, h / 800)
        scale = max(0.7, min(scale, 1.5))

        card_grad = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fffbe7, stop:1 #ffe082)"
        title_color = "#b28704"
        label_color = "#795548"
        input_bg = "#fffde7"
        input_border = "#ffd54f"
        input_text = "#795548"
        list_bg = "#fffde7"
        list_border = "#ffd54f"

        self.setStyleSheet(f"background: #fffde7;")
        self.card_frame.setMaximumWidth(int(self.width() * 0.98))
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

        # Fix: Pass username to encrypt_data if required by your encryption.py
        try:
            encrypt_data(content, enc_path, self.username)
        except TypeError:
            # For backward compatibility if encrypt_data expects only 2 args
            encrypt_data(content, enc_path)
        except Exception as e:
            QMessageBox.critical(self, "Encryption Error", f"Failed to encrypt entry: {str(e)}")
            return

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


