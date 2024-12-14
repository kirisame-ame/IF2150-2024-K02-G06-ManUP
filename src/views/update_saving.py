import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal
from controllers.savingC import create_saving

class SavingFormEditUI(QWidget):
    closed = pyqtSignal()

    def __init__(self, budget_ui, saving_id):
        super().__init__()
        self.budget_ui = budget_ui
        self.saving_id = saving_id
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)

        self.target_label = QLabel("Target Amount:")
        self.target_input = QLineEdit()
        layout.addWidget(self.target_label)
        layout.addWidget(self.target_input)

        self.start_date_label = QLabel("Start Date (YYYY-MM-DD):")
        self.start_date_input = QLineEdit()
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_input)

        self.end_date_label = QLabel("End Date (YYYY-MM-DD):")
        self.end_date_input = QLineEdit()
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_form)
        layout.addWidget(self.submit_button)

    def submit_form(self):
        try:
            current_amount = float(self.amount_input.text())
            target_amount = float(self.target_input.text())
            start_date = self.start_date_input.text()
            target_date = self.end_date_input.text()

            data = {
                "id": self.saving_id,
                "currentAmount": current_amount,
                "targetAmount": target_amount,
                "startDate": start_date,
                "targetDate": target_date
            }

            # Update data saving
            create_saving(data)

            # Refresh UI and close form
            self.hide()
            self.budget_ui.refresh_ui()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please ensure all fields are correctly filled.")

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
