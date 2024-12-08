from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
)

class Navbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Navigation bar
        nav_bar = QHBoxLayout(self)
        self.btn_home = QPushButton("Home")
        self.btn_transaction = QPushButton("Transactions")
        self.btn_budget = QPushButton("Budget")

        # Add buttons to the nav bar
        nav_bar.addWidget(self.btn_transaction)
        nav_bar.addWidget(self.btn_home)
        nav_bar.addWidget(self.btn_budget)

        # Add nav bar to the main layout

        # Set styling
        self.setStyleSheet(
            """
            QPushButton {
                color:black;
                font-size: 16px;
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #000000;
            }
            """
        )