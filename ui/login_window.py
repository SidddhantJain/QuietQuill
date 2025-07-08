from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test LoginWindow")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Login UI working"))
        self.setLayout(layout)
