# src/views/transaction.py
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from controllers.transactionC import read_transaction
# from views.form_transaction import TransactionFormUI
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

        self.delete_button = QPushButton("Delete Transaction")
        self.delete_button.clicked.connect(self.form_delete_transaction)

        self.update_button = QPushButton("Update Transaction")
        self.update_button.clicked.connect(self.form_update_transaction)

        self.form_create_button = QPushButton("Form Create Transaction")
        self.form_create_button.clicked.connect(self.form_create_transaction)

        # Add buttons to the main layout
        main_layout.addWidget(self.read_button)
        main_layout.addWidget(self.form_create_button)
        main_layout.addWidget(self.delete_button)
        main_layout.addWidget(self.update_button)

    def read_transactions(self):
        transactions = read_transaction()
        if not transactions.empty:
            table_html = """
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    <th>ID</th>
                    <th>Amount</th>
                    <th>Date</th>
                    <th>Type</th>
                    <th>Description</th>
                </tr>
            """
            for t in transactions.to_dict('records'):
                table_html += f"""
                <tr>
                    <td>{t['id']}</td>
                    <td>{t['amount']}</td>
                    <td>{t['date']}</td>
                    <td>{t['type']}</td>
                    <td>{t['description']}</td>
                </tr>
                """
            table_html += "</table>"
            self.content.setText(table_html)
        else:
            self.content.setText("No transactions found.")
        self.content.setStyleSheet(
            """
            QLabel {
                margin-top: 20px;
                text-align: left;
                color: blue;
                font-size: 14px;
                padding: 10px;
                border: 1px solid black;
                background-color: #f0f0f0;
            }
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid black;
                padding: 5px;
                text-align: left;
            }
            th {
                background-color: #f0f0f0;
            }
            """
        )

    def form_delete_transaction(self):
        from views.delete_transaction import TransactionDeleteUI
        self.form = TransactionDeleteUI(self)
        self.form.show()

    def form_update_transaction(self):
        from views.update_transaction import TransactionFormEditUI
        self.form = TransactionFormEditUI(self)
        self.form.show()
        
    def form_create_transaction(self):
        from views.create_transaction import TransactionFormUI
        self.form = TransactionFormUI(self)
        self.form.show()
    