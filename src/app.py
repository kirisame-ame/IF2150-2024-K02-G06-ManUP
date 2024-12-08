import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from PyQt6.QtWidgets import QApplication, QMainWindow
from views.home import HomeUI
from views.components.navbar import Navbar
from views.transaction import TransactionUI

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

    def show_home(self):
        self.view.content.setText("Welcome to the Home Page!")

    def show_transactions(self):
        self.setCentralWidget(self.transaction_ui)

    def show_budget(self):
        self.view.content.setText("This is the Budget Page.")

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
