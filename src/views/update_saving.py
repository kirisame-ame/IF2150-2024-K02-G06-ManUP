# src/views/form_transaction.py
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from controllers.savingC import updateCurrentAmount
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import pyqtSignal
import re
from PyQt6.QtWidgets import QMessageBox
class UpdateSavingFormUI(QWidget):
    closed = pyqtSignal()
    def __init__(self, saving_ui, id):
        super().__init__()
        self.saving_ui = saving_ui
        self.id = id
        self.setup_ui()

    def setup_ui(self):
        input_layout = QVBoxLayout(self)

        self.amount_label = QLabel("Add Amount: ")
        self.amount_input = QLineEdit()
        input_layout.addWidget(self.amount_label)
        input_layout.addWidget(self.amount_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.form_create_saving)
        input_layout.addWidget(self.submit_button)
        
        self.setLayout(input_layout)
        
    def form_create_saving(self):
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            self.show_error_message("Amount must be a number")
            return


# Ambil year, month, dan day
        id = self.id
        updateCurrentAmount(id, amount)
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

    