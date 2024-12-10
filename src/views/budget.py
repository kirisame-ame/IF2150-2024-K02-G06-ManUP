from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt  # Import Qt.AlignmentFlag
from views.components.navbar import Navbar


class BudgetUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)

        # Add navbar
        self.navbar = Navbar()
        main_layout.addWidget(self.navbar)

        # Content layout split into two halves
        content_layout = QHBoxLayout()

        # Savings section
        savings_section = QFrame()
        savings_layout = QVBoxLayout(savings_section)
        savings_label = QLabel("Savings")
        savings_label.setStyleSheet("font-size: 18px; font-weight: bold; text-align: center;")
        savings_amount = QLabel("$5000")  # Example value
        savings_amount.setStyleSheet("font-size: 24px; color: green; text-align: center;")
        # Center contents of the savings layout
        savings_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        savings_layout.addWidget(savings_label, alignment=Qt.AlignmentFlag.AlignCenter)
        savings_layout.addWidget(savings_amount, alignment=Qt.AlignmentFlag.AlignCenter)
        savings_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Budget section
        budget_section = QFrame()
        budget_layout = QVBoxLayout(budget_section)
        budget_label = QLabel("Budget")
        budget_label.setStyleSheet("font-size: 18px; font-weight: bold; text-align: center;")
        budget_amount = QLabel("$10000")  # Example value
        budget_amount.setStyleSheet("font-size: 24px; color: blue; text-align: center;")
        # Center contents of the budget layout
        budget_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        budget_layout.addWidget(budget_label, alignment=Qt.AlignmentFlag.AlignCenter)
        budget_layout.addWidget(budget_amount, alignment=Qt.AlignmentFlag.AlignCenter)
        budget_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Add savings and budget sections to the content layout
        content_layout.addWidget(savings_section)
        content_layout.addWidget(budget_section)

        # Add content layout to the main layout
        main_layout.addLayout(content_layout)

        # Set styling
        self.setStyleSheet(
            """
            QLabel {
                text-align: center;
            }
            """
        )
