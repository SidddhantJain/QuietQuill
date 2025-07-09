from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QComboBox, QDateEdit, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtCore import QDate
import os, json

class AdvancedSearchWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("🔍 Advanced Search")
        self.setGeometry(600, 300, 500, 500)
        self.entry_dir = os.path.join("entries", username)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Keyword input
        layout.addWidget(QLabel("🔑 Keyword:"))
        self.keyword_input = QLineEdit()
        layout.addWidget(self.keyword_input)

        # Date range
        date_row = QHBoxLayout()
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        self.start_date.setDate(QDate.currentDate().addMonths(-1))

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        self.end_date.setDate(QDate.currentDate())

        date_row.addWidget(QLabel("📅 From:"))
        date_row.addWidget(self.start_date)
        date_row.addWidget(QLabel("To:"))
        date_row.addWidget(self.end_date)
        layout.addLayout(date_row)

        # Tag input
        layout.addWidget(QLabel("🏷️ Tag (optional):"))
        self.tag_input = QLineEdit()
        layout.addWidget(self.tag_input)

        # Content type
        layout.addWidget(QLabel("📁 Content Type:"))
        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Any", "Text only", "With Image"])
        layout.addWidget(self.type_dropdown)

        # Search button
        self.search_btn = QPushButton("🔍 Search")
        self.search_btn.clicked.connect(self.perform_search)
        layout.addWidget(self.search_btn)

        # Results list
        self.result_list = QListWidget()
        layout.addWidget(self.result_list)

        self.setLayout(layout)

    def perform_search(self):
        self.result_list.clear()
        keyword = self.keyword_input.text().lower()
        tag = self.tag_input.text().lower()
        type_filter = self.type_dropdown.currentText()
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")

        results = []
        for file in os.listdir(self.entry_dir):
            if file.endswith(".meta.json"):
                meta_path = os.path.join(self.entry_dir, file)
                with open(meta_path, "r") as f:
                    meta = json.load(f)

                date = meta.get("date", "")
                if not (start_date <= date <= end_date):
                    continue

                title = meta.get("title", "").lower()
                content = meta.get("preview", "").lower()
                tags = [t.lower() for t in meta.get("tags", [])]
                has_image = meta.get("has_image", False)

                # Content type check
                if type_filter == "Text only" and has_image:
                    continue
                elif type_filter == "With Image" and not has_image:
                    continue

                # Keyword check
                if keyword and keyword not in title and keyword not in content:
                    continue

                # Tag check
                if tag and tag not in tags:
                    continue

                results.append((date, meta.get("title", "Untitled Entry"), meta_path.replace(".meta.json", ".enc")))

        if results:
            for date, title, path in results:
                item = QListWidgetItem(f"{date} - {title}")
                item.setData(1000, path)
                self.result_list.addItem(item)
        else:
            QMessageBox.information(self, "No Results", "No entries matched your search.")
