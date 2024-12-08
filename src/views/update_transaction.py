# src/views/form_transaction.py
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from controllers.transactionC import update_transaction
from PyQt6.QtWidgets import QComboBox
class TransactionFormEditUI(QWidget):
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
        
        self.date_label = QLabel("Date:")
        self.date_input = QLineEdit()
        input_layout.addWidget(self.date_label)
        input_layout.addWidget(self.date_input)
        
        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()
        input_layout.addWidget(self.amount_label)
        input_layout.addWidget(self.amount_input)
        
        self.type_label = QLabel("Type:")
        self.type_input = QComboBox()
        self.type_input.addItems(["expense", "income"])
        input_layout.addWidget(self.type_label)
        input_layout.addWidget(self.type_input)
        
        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        input_layout.addWidget(self.description_label)
        input_layout.addWidget(self.description_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.form_update_transaction)
        input_layout.addWidget(self.submit_button)
        
        self.setLayout(input_layout)
        
    def form_update_transaction(self):
        id = int(self.id_input.text())
        amount = float(self.amount_input.text())
        date = self.date_input.text()
        type = self.type_input.currentText()
        description = self.description_input.text()
        
        data = {'id': id, 'amount': amount, 'date': date, 'type': type, 'description': description}
        update_transaction(data)
        self.hide()
        self.transaction_ui.show()

    