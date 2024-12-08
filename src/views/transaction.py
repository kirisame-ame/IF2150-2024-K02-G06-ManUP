# src/views/transaction.py
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from controllers.transactionC import read_transaction
from controllers.transactionC import create_transaction
from controllers.transactionC import delete_transaction
from controllers.transactionC import update_transaction
from controllers.transactionC import get_transaction
from controllers.transactionC import getNewId

from views.components.navbar import Navbar
class TransactionUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)

        # add navbar
        self.navbar = Navbar()
        main_layout.addWidget(self.navbar)
        # Central content placeholder
        self.content = QLabel("This is the Transactions Page.")

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
        # Add buttons to interact with the controller
        self.read_button = QPushButton("Read Transactions")
        self.read_button.clicked.connect(self.read_transactions)

        self.create_button = QPushButton("Create Transaction")
        self.create_button.clicked.connect(self.create_transaction)

        self.delete_button = QPushButton("Delete Transaction")
        self.delete_button.clicked.connect(self.delete_transaction)

        self.update_button = QPushButton("Update Transaction")
        self.update_button.clicked.connect(self.update_transaction)

        # Add buttons to the main layout
        main_layout.addWidget(self.read_button)
        main_layout.addWidget(self.create_button)
        main_layout.addWidget(self.delete_button)
        main_layout.addWidget(self.update_button)

    def read_transactions(self):
        transactions = read_transaction()
        self.content.setText(str(transactions))

    def create_transaction(self):
        id = getNewId()
        data = {'id': id, 'amount': 20, 'date': '2023-10-01', 'type': 'income', 'description': 'Sample'}
        transactions = create_transaction(data)
        self.content.setText(str(transactions))

    def delete_transaction(self):
        transactions = delete_transaction(1)
        self.content.setText(str(transactions))

    def update_transaction(self):
        data = {'id': 1, 'amount': 20, 'date': '2023-10-01', 'type': 'income', 'description': 'Sample'}
        transactions = update_transaction(data)
        self.content.setText(str(transactions))