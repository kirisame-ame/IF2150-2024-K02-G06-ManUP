# src/app.py
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from views.home import HomeUI
from views.components.navbar import Navbar
from views.transaction import TransactionUI
from views.budget import BudgetUI

class HomeController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ManUP Budgeting App")
        
        # Create a central widget to hold other widgets
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create layouts
        self.main_layout = QVBoxLayout(self.central_widget)

        # Initialize the UIs once
        self.transaction_ui = TransactionUI()
        self.home_ui = HomeUI()
        self.budget_ui = BudgetUI()
        
        # Initially show home UI
        self.current_ui = self.home_ui
        self.main_layout.addWidget(self.current_ui)

        # Connect buttons to methods
        self.connect_navbar(self.home_ui.navbar)
        self.connect_navbar(self.transaction_ui.navbar)
        self.connect_navbar(self.budget_ui.navbar)

    def connect_navbar(self, navbar):
        navbar.btn_transaction.clicked.connect(self.show_transactions)
        navbar.btn_home.clicked.connect(self.show_home)
        navbar.btn_budget.clicked.connect(self.show_budget)
        
    def show_home(self):
        self._switch_ui(self.home_ui)

    def show_transactions(self):
        self._switch_ui(self.transaction_ui)

    def show_budget(self):
        self._switch_ui(self.budget_ui)

    def _switch_ui(self, new_ui):
        # Remove the current UI
        self.main_layout.removeWidget(self.current_ui)
        self.current_ui.hide()
        
        # Add the new UI
        self.current_ui = new_ui
        self.main_layout.addWidget(self.current_ui)
        self.current_ui.show()

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow{
            background-color: #f0f0f0;           
        }
       """)
    controller = HomeController()
    controller.resize(800, 600)
    controller.show()
    sys.exit(app.exec())