# src/views/budget.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
)
import views.components.navbar as navbar

class BudgetUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)

        # Central content placeholder
        self.content = QLabel("Welcome to the Budget Page!!!")

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
