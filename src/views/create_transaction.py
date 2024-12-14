# src/views/form_transaction.py
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
import pandas as pd
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from controllers.transactionC import create_transaction
from controllers.transactionC import getNewId
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import pyqtSignal
import re
from PyQt6.QtWidgets import QMessageBox
from controllers.transactionC import read_transaction
class TransactionFormUI(QWidget):
    closed = pyqtSignal()
    def __init__(self, transaction_ui):
        super().__init__()
        self.transaction_ui = transaction_ui
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: black;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                padding: 10px;
                font-size: 14px;
                background-color: #4CAF50; 
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        input_layout = QVBoxLayout(self)

        self.date_label = QLabel("Date (YYYY-MM-DD):")
        self.date_input = QLineEdit()
        self.date_input.setStyleSheet("color: black;")
        input_layout.addWidget(self.date_label)
        input_layout.addWidget(self.date_input)
        
        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()
        self.amount_input.setStyleSheet("color: black;")
        input_layout.addWidget(self.amount_label)
        input_layout.addWidget(self.amount_input)
        
        self.type_label = QLabel("Type:")
        self.type_input = QComboBox()
        self.type_input.setStyleSheet("color: black;")
        self.type_input.addItems(["Select Type", "expense", "income"])
        self.type_input.currentTextChanged.connect(self.update_category)
        self.type_input.currentIndexChanged.connect(self.remove_select_type)
        input_layout.addWidget(self.type_label)
        input_layout.addWidget(self.type_input)
        
        self.category_label = QLabel("Category:")
        self.category_input = QComboBox()
        self.category_input.setStyleSheet("color: black;")
        input_layout.addWidget(self.category_label)
        input_layout.addWidget(self.category_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.form_create_transaction)
        input_layout.addWidget(self.submit_button)
        
        self.setLayout(input_layout)
        
    def form_create_transaction(self):
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        date = self.date_input.text()
        if not date_pattern.match(date):
            self.show_error_message("Date must be in format YYYY-MM-DD")
            return
        
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            self.show_error_message("Amount must be a number")
            return
        
        id = getNewId()
        type = self.type_input.currentText()
        category = self.category_input.currentText()
        
        data = {'id': id, 'amount': amount, 'date': date, 'type': type, 'category': category}
        budget_data = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))
        if (type == 'expense'):
            budget_data.loc[budget_data['budgetName'] == category, 'budgetAmount'] -= amount
            budget_data.to_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'), index=False)
        create_transaction(data)
        self.hide()
        self.transaction_ui.load_transactions()
        self.transaction_ui.show()

    def show_error_message(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Input Error")
        error_dialog.exec()
    
    def remove_select_type(self, text):
        if text != "Select Type" and self.type_input.findText("Select Type") != -1:
            self.type_input.removeItem(self.type_input.findText("Select Type"))
    def update_category(self, text):
        if text == "Select Type":
            self.category_input.clear()
        elif text == "expense":
            self.category_input.clear()
            self.category_input.addItems(["food", "transport", "bills", "shopping", "other"])
        elif text == "income":
            self.category_input.clear()
            self.category_input.addItems(["job", "side jobs", "investments", "gifts", "other"])
    # def form_create_transaction(self):
    #     id = getNewId()
    #     amount = float(self.amount_input.text())
    #     date = self.date_input.text()
    #     type = self.type_input.currentText()
    #     category = self.category_input.currentText()
        
    #     data = {'id': id, 'amount': amount, 'date': date, 'type': type, 'category': category}
    #     create_transaction(data)
    #     self.hide()
    #     self.transaction_ui.load_transactions()
    #     self.transaction_ui.show()

    