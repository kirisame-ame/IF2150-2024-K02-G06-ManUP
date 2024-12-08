# src/app.py
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from PyQt6.QtWidgets import QApplication, QMainWindow
from views.home import HomeUI
from views.components.navbar import Navbar
from views.transaction import TransactionUI
from views.budget import BudgetUI
class HomeController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ManUP Budgeting App")

        # Initialize the UI
        self.view = HomeUI()
        self.setCentralWidget(self.view)

        # Connect buttons to methods
        self.navbar = Navbar()
        self.view.layout().setMenuBar(self.navbar)
        self.navbar.btn_transaction.clicked.connect(self.show_transactions)
        self.navbar.btn_home.clicked.connect(self.show_home)
        self.navbar.btn_budget.clicked.connect(self.show_budget)

        # Initialize the transaction UI
        self.transaction_ui = TransactionUI()
        self.home_ui = HomeUI()
        self.budget_ui = BudgetUI()

    def show_home(self):
        self.setCentralWidget(self.home_ui)

    def show_transactions(self):
        self.setCentralWidget(self.transaction_ui)

    def show_budget(self):
        self.setCentralWidget(self.budget_ui)
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
