from PyQt5.QtWidgets import (
    QWidget, QTextEdit, QPushButton, QVBoxLayout, QLabel,
    QFileDialog, QMessageBox, QLineEdit
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
import base64
from datetime import datetime
from utils.encryption import encrypt_data, decrypt_data

class EditorWindow(QWidget):
    def __init__(self, username, filename=None):
        super().__init__()
        self.username = username
        self.filename = filename
        self.setWindowTitle("QuietQuill - New Entry" if not filename else f"QuietQuill - {filename}")
        self.setGeometry(250, 180, 700, 550)

        self.init_ui()

        if self.filename:
            self.load_entry()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Optional: Title for your entry")

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Start writing your thoughts here...")

        self.image_button = QPushButton("📷 Insert Image")
        self.image_button.clicked.connect(self.insert_image)

        self.save_button = QPushButton("💾 Save Entry")
        self.save_button.clicked.connect(self.save_entry)

        layout.addWidget(QLabel(f"<h3>{'📝 New Entry' if not self.filename else '📂 Editing Entry'}</h3>"))
        layout.addWidget(self.title_input)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.image_button)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def insert_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Insert Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            try:
                with open(file_path, "rb") as img_file:
                    encoded = base64.b64encode(img_file.read()).decode()
                    ext = os.path.splitext(file_path)[-1][1:]  # e.g. 'jpg'
                    img_tag = f'<img src="data:image/{ext};base64,{encoded}" width="400"><br><br>'
                    self.text_edit.insertHtml(img_tag)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to insert image: {str(e)}")

    def save_entry(self):
        content = self.text_edit.toHtml()
        encrypted = encrypt_data(content, self.username)

        if not self.filename:
            title = self.title_input.text().strip().replace(" ", "_") or "entry"
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.filename = f"{timestamp}_{title}.enc"

        entry_path = os.path.join("entries", self.username)
        os.makedirs(entry_path, exist_ok=True)

        filepath = os.path.join(entry_path, self.filename)
        try:
            with open(filepath, "wb") as f:
                f.write(encrypted)
            QMessageBox.information(self, "Saved", "Your diary entry was saved successfully.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save entry: {str(e)}")

    def load_entry(self):
        filepath = os.path.join("entries", self.username, self.filename)
        try:
            with open(filepath, "rb") as f:
                encrypted = f.read()
            decrypted = decrypt_data(encrypted, self.username)
            self.text_edit.setHtml(decrypted)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load entry: {str(e)}")
