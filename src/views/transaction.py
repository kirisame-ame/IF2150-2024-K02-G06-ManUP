import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt6.QtCore import Qt
from controllers.transactionC import read_transaction, delete_transaction, update_transaction

from views.components.navbar import Navbar
class TransactionUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_transactions()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # add navbar
        self.navbar = Navbar()
        main_layout.addWidget(self.navbar)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        self.create_button = QPushButton("Create Transaction")
        self.create_button.clicked.connect(self.open_create_form)

        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.create_button)

    def load_transactions(self):
        transactions = read_transaction()
        self.clear_transaction_cards()
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for t in transactions.to_dict('records'):
            transaction_widget = self.create_transaction_card(t)
            self.scroll_layout.addWidget(transaction_widget)

    def clear_transaction_cards(self):
        while self.scroll_layout.count() > 0:
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def create_transaction_card(self, transaction):
        card = QWidget()
        card_layout = QVBoxLayout(card)

        header_layout = QHBoxLayout()
        category_label = QLabel(transaction['category'])
        date_label = QLabel(transaction['date'])
        header_layout.addWidget(category_label)
        header_layout.addWidget(date_label, alignment=Qt.AlignmentFlag.AlignRight)

        amount_label = QLabel(f"Rp {transaction['amount']}")
        amount_label.setStyleSheet("font-weight: bold;")

        button_layout = QHBoxLayout()
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_transaction(transaction['id']))
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda: self.edit_transaction(transaction['id']))
        button_layout.addWidget(delete_button)
        button_layout.addWidget(edit_button)

        card_layout.addLayout(header_layout)
        card_layout.addWidget(amount_label, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addLayout(button_layout)

        return card

    def delete_transaction(self, id):
        delete_transaction(id)
        self.load_transactions()

    def edit_transaction(self, id):
        from views.update_transaction import TransactionFormEditUI
        self.edit_form = TransactionFormEditUI(self, id)
        self.edit_form.show()
        self.edit_form.closed.connect(self.load_transactions)

    def open_create_form(self):
        from views.create_transaction import TransactionFormUI
        self.create_form = TransactionFormUI(self)
        self.create_form.show()
        self.create_form.closed.connect(self.load_transactions)