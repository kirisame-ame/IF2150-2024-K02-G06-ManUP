import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt6.QtGui import QPixmap
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
        card_layout = QHBoxLayout(card)
        card.setStyleSheet("border: 1px solid gray; border-radius: 5px; padding: 2px;")

        # Bagian Kiri: Logo
        logo_label = QLabel()
        logo_label.setFixedSize(65, 65)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if transaction['type'] == 'expense':
            logo_label.setStyleSheet("background-color: red;")
        else:
            logo_label.setStyleSheet("background-color: green;")
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
        category_label.setStyleSheet("font-size: 10px; font-weight: bold; margin-top: 2.5px;")
        category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        category_label.setFixedWidth(65)  # Sesuaikan lebar teks dengan lebar logo
        left_layout.addWidget(category_label)

        card_layout.addLayout(left_layout)
        # Bagian Tengah: Amount dan Tombol
        center_layout = QVBoxLayout()
        # Amount
        amount_label = QLabel(f"Rp {transaction['amount']}")
        if transaction['type'] == 'expense':
            amount_label.setStyleSheet("color: red; font-weight: bold; font-size: 16px;")
        else:
            amount_label.setStyleSheet("color: green; font-weight: bold; font-size: 16px;")
        center_layout.addWidget(amount_label)

        # Tombol Delete dan Edit
        button_layout = QHBoxLayout()
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_transaction(transaction['id']))
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda: self.edit_transaction(transaction['id']))
        button_layout.addWidget(delete_button)
        button_layout.addWidget(edit_button)
        center_layout.addLayout(button_layout)

        card_layout.addLayout(center_layout)

        # Bagian Kanan: Date
        date_label = QLabel(f"Date: {transaction['date']}")
        date_label.setStyleSheet("font-size: 30px; color: white; background-color: gray; padding: 5px; border-radius: 5px;")
        date_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        card_layout.addWidget(date_label)

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