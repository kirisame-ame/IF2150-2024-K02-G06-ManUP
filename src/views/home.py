import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QMessageBox, QInputDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from controllers.homeC import get_four_most_recent_transaction, pie_chart_for_category_in_type_expense, remainder
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
)
from views.components.navbar import Navbar
import matplotlib.pyplot as plt
from views.budget import BudgetUI
from views.create_transaction import TransactionFormUI
from views.update_transaction import TransactionFormEditUI
from views.transaction import TransactionUI
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class HomeUI(QWidget):
    def __init__(self):
        super().__init__()
        self.budget_ui = BudgetUI()
        self.transaction_ui = TransactionUI()
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)

        # add navbar
        self.navbar = Navbar()
        main_layout.addWidget(self.navbar)

        split_layout = QHBoxLayout()
        main_layout.addLayout(split_layout)

        # Left frame for pie chart
        left_frame = QVBoxLayout()
        split_layout.addLayout(left_frame)

        # Add pie chart to the left frame
        self.pie_chart_label = QLabel()
        self.pie_chart_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_frame.addWidget(self.pie_chart_label)

        # Right frame for list of transaction cards
        right_frame = QVBoxLayout()
        split_layout.addLayout(right_frame)

        # Add four most recent transactions to the right frame
        self.recent_transactions_layout = QVBoxLayout()
        right_frame.addLayout(self.recent_transactions_layout)

        self.budget_ui.budget_updated.connect(self.update_pie_chart)
        self.transaction_ui.transaction_updated.connect(self.update_recent_transactions)
        self.update_pie_chart()
        self.update_recent_transactions()

    def showEvent(self, event):
        super().showEvent(event)
        self.update_pie_chart()
        self.update_recent_transactions()

    def update_pie_chart(self):
        figure = pie_chart_for_category_in_type_expense()
        canvas = FigureCanvas(figure)
        self.pie_chart_label.setPixmap(QPixmap())
        layout = self.pie_chart_label.layout()
        if layout is None:
            layout = QVBoxLayout(self.pie_chart_label)
        else:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        layout.addWidget(canvas)

    def update_recent_transactions(self):
        # Clear previous transaction cards
        for i in reversed(range(self.recent_transactions_layout.count())):
            self.recent_transactions_layout.itemAt(i).widget().deleteLater()

        transactions = get_four_most_recent_transaction()
        for transaction in transactions:
            card = self.create_transaction_card(transaction)
            self.recent_transactions_layout.addWidget(card)

    def show_recent_transactions(self):
        transactions = get_four_most_recent_transaction()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        for transaction in transactions:
            card = self.create_transaction_card(transaction)
            scroll_layout.addWidget(card)

        scroll_area.setWidget(scroll_content)

        msg = QMessageBox()
        msg.setWindowTitle("Recent Transactions")
        msg.layout().addWidget(scroll_area)
        msg.exec()

    def reset_widget_after_the_transaction_updated(self):
        self.update_pie_chart()
        self.update_recent_transactions()

    def reset_widget_after_the_budget_updated(self):
        self.update_pie_chart()
        self.update_recent_transactions()

    def create_transaction_card(self, transaction):
        card = QWidget()
        card_layout = QHBoxLayout(card)
        card.setStyleSheet("border: 1px solid gray; border-radius: 5px; padding: 2px;")

        # Bagian Kiri: Logo
        logo_label = QLabel()
        logo_label.setFixedSize(65, 65)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if transaction['type'] == 'expense':
            logo_label.setStyleSheet("background-color: #e80b67;")
        else:
            logo_label.setStyleSheet("background-color: #02b429;")
        category = transaction['category']
        logo_path = os.path.join(os.getcwd(), 'src', 'public', f'{category}.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap.scaled(65, 65, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_label.setText("No Logo")
        
        left_layout = QVBoxLayout()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(logo_label)

        category_label = QLabel(f"{transaction['category']}")
        if transaction['type'] == 'expense':
            category_label.setStyleSheet("font-size: 10px; font-weight: bold; margin-top: 2.5px; color: white; background-color: #e80b67;")
        else:
            category_label.setStyleSheet("font-size: 10px; font-weight: bold; margin-top: 2.5px; color: white; background-color: #02b429;")
        category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        category_label.setFixedWidth(65)  # Sesuaikan lebar teks dengan lebar logo
        left_layout.addWidget(category_label)

        card_layout.addLayout(left_layout)
        # Bagian Tengah: Amount dan Tombol
        center_layout = QVBoxLayout()
        # Amount
        amount_label = QLabel(f"Rp {transaction['amount']}")
        if transaction['type'] == 'expense':
            amount_label.setStyleSheet("color: #e80b67; font-weight: bold; font-size: 16px;")
        else:
            amount_label.setStyleSheet("color: #02b429; font-weight: bold; font-size: 16px;")
        center_layout.addWidget(amount_label)

        card_layout.addLayout(center_layout)

        # Bagian Kanan: Date
        date_label = QLabel(f"Date: {transaction['date']}")
        date_label.setStyleSheet("font-size: 30px; color: white; background-color: gray; padding: 5px; border-radius: 5px;")
        date_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        card_layout.addWidget(date_label)

        return card

    def reset_widget(self):
        self.reset_widget_after_the_transaction_updated()
        self.reset_widget_after_the_budget_updated()
