# src/views/form_transaction.py
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from controllers.transactionC import delete_transaction
class TransactionDeleteUI(QWidget):
    def __init__(self, transaction_ui):
        super().__init__()
        self.transaction_ui = transaction_ui
        self.setup_ui()

    def setup_ui(self):
        input_layout = QVBoxLayout(self)

        self.id_label = QLabel("ID:")
        self.id_input = QLineEdit()
        input_layout.addWidget(self.id_label)
        input_layout.addWidget(self.id_input)
        
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.form_delete_transaction)
        input_layout.addWidget(submit_button)
        
        self.setLayout(input_layout)
        
    def form_delete_transaction(self):
        id = int(self.id_input.text())
        
        delete_transaction(id)
        self.hide()
        self.transaction_ui.show()

    