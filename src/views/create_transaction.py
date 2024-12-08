# src/views/form_transaction.py
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from controllers.transactionC import create_transaction
from controllers.transactionC import getNewId
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import pyqtSignal
class TransactionFormUI(QWidget):
    closed = pyqtSignal()
    def __init__(self, transaction_ui):
        super().__init__()
        self.transaction_ui = transaction_ui
        self.setup_ui()

    def setup_ui(self):
        input_layout = QVBoxLayout(self)

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
        self.type_input.addItems(["Select Type", "expense", "income"])
        self.type_input.currentTextChanged.connect(self.update_category)
        self.type_input.currentTextChanged.connect(self.remove_select_type)
        input_layout.addWidget(self.type_label)
        input_layout.addWidget(self.type_input)
        
        self.category_label = QLabel("Category:")
        self.category_input = QComboBox()
        input_layout.addWidget(self.category_label)
        input_layout.addWidget(self.category_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.form_create_transaction)
        input_layout.addWidget(self.submit_button)
        
        self.setLayout(input_layout)
    
    def remove_select_type(self, text):
        if text != "Select Type":
            self.type_input.removeItem(0)
    def update_category(self, text):
        self.category_input.clear()
        if text == "expense":
            self.category_input.addItems(["food", "transport", "bills", "shopping", "other"])
        elif text == "income":
            self.category_input.addItems(["job", "side jobs", "investments", "gifts", "other"])
    def form_create_transaction(self):
        id = getNewId()
        amount = float(self.amount_input.text())
        date = self.date_input.text()
        type = self.type_input.currentText()
        category = self.category_input.currentText()
        
        data = {'id': id, 'amount': amount, 'date': date, 'type': type, 'category': category}
        create_transaction(data)
        self.hide()
        self.transaction_ui.load_transactions()
        self.transaction_ui.show()

    