# src/views/budget.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
)
from views.components.navbar import Navbar

class BudgetUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)

        # Central content placeholder
        self.content = QLabel("Welcome to the Budget Page!!!")

        # add navbar
        self.navbar = Navbar()
        main_layout.addWidget(self.navbar)
        
        # Add nav bar and content to the main layout
        main_layout.addWidget(self.content)

        # Set styling
        self.setStyleSheet(
            """
            QLabel {
                margin-top: 20px;
                text-align: center;
                color:black;
            }
            """
        )
