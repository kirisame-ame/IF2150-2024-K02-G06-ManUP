# src/views/form_transaction.py
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from controllers.savingC import getNewIdS, create_saving
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import pyqtSignal
import re
from PyQt6.QtWidgets import QMessageBox
from datetime import date
class SavingFormUI(QWidget):
    closed = pyqtSignal()
    def __init__(self, saving_ui):
        super().__init__()
        self.saving_ui = saving_ui
        self.setup_ui()

    def setup_ui(self):
        input_layout = QVBoxLayout(self)

        self.date_label = QLabel("Date (YYYY-MM-DD):")
        self.date_input = QLineEdit()
        input_layout.addWidget(self.date_label)
        input_layout.addWidget(self.date_input)


        self.amount_label = QLabel("Target Amount: ")
        self.amount_input = QLineEdit()
        input_layout.addWidget(self.amount_label)
        input_layout.addWidget(self.amount_input)
        

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.form_create_saving)
        input_layout.addWidget(self.submit_button)
        
        self.setLayout(input_layout)
        
    def form_create_saving(self):
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        dateIn = self.date_input.text()
        if not date_pattern.match(dateIn):
            self.show_error_message("Date must be in format YYYY-MM-DD")
            return
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            self.show_error_message("Amount must be a number")
            return
        
        id = getNewIdS()
        current_date = date.today()

# Ambil year, month, dan day
        current_year = current_date.year
        current_month = current_date.month
        current_day = current_date.day
        str_date = str(current_year)+"-"+str(current_month)+"-"+str(current_day)
        data = {'id': id, 'currentAmount': 0, 'startDate': str_date, 'targetDate': dateIn, "targetAmount": amount}
        create_saving(data)
        self.hide()
        self.saving_ui.load_savings()
        self.saving_ui.show()

    def show_error_message(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Input Error")
        error_dialog.exec()


    #     id = getNewId()s
    #     amount = float(self.amount_input.text())
    #     date = self.date_input.text()
    #     type = self.type_input.currentText()
    #     category = self.category_input.currentText()
        
    #     data = {'id': id, 'amount': amount, 'date': date, 'type': type, 'category': category}
    #     create_transaction(data)
    #     self.hide()
    #     self.transaction_ui.load_transactions()
    #     self.transaction_ui.show()

    