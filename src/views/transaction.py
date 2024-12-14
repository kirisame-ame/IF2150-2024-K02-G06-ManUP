import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QMessageBox, QInputDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from controllers.transactionC import read_transaction, delete_transaction, get_transaction_by_type, get_transaction_by_category, get_transaction_by_date, sort_transaction_by_date_asc, sort_transaction_by_date_desc
from PyQt6.QtCore import pyqtSignal
from views.components.navbar import Navbar
from views.budget import BudgetUI
class TransactionUI(QWidget):
    transaction_updated = pyqtSignal()
    refresh_budget = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: white;
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
                background-color: #1CD43A;
                border: none;
                color: white;
                
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.setup_ui()
        self.load_transactions()
        self.budget_ui = BudgetUI()
        
                # Hubungkan sinyal budget_updated ke refresh method
        self.budget_ui.budget_updated.connect(self.refresh_budget_view)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # add navbar
        self.navbar = Navbar()
        main_layout.addWidget(self.navbar)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        self.create_button = QPushButton("Create Transaction")
        self.create_button.clicked.connect(self.open_create_form)

        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.create_button)
        filter_layout = QHBoxLayout()

        self.type_filter = QPushButton("Filter by Type")
        self.type_filter.clicked.connect(self.filter_by_type)
        filter_layout.addWidget(self.type_filter)

        self.category_filter = QPushButton("Filter by Category")
        self.category_filter.clicked.connect(self.filter_by_category)
        filter_layout.addWidget(self.category_filter)

        self.sort_date_button = QPushButton("Sort by Date")
        self.sort_date_button.clicked.connect(self.sort_by_date)
        
        filter_layout.addWidget(self.sort_date_button)

        self.date_filter = QPushButton("Clear Filter")
        self.date_filter.clicked.connect(self.clear_filter)
        filter_layout.addWidget(self.date_filter)

        main_layout.addLayout(filter_layout)

    def filter_by_type(self):
        types = ["expense", "income"]
        input_dialog = QInputDialog(self)
        input_dialog.setWindowTitle("Filter by Type")
        input_dialog.setLabelText("Select transaction type:")
        input_dialog.setComboBoxItems(types)
        input_dialog.setStyleSheet("QLabel { color: black; } QLineEdit { color: black; } QComboBox { color: black; }")

        if input_dialog.exec() == QInputDialog.DialogCode.Accepted:
            type = input_dialog.textValue()
            transactions = get_transaction_by_type(type)
            self.display_filtered_transactions(transactions)

    def filter_by_category(self):
        categories = ["food", "transport", "bills", "shopping", "other","job", "side jobs", "investments", "gifts"]
        category, ok = QInputDialog.getItem(self, 'Filter by Category', 'Select transaction category:', categories, 0, False)
        if ok and category:
            transactions = get_transaction_by_category(category)
            self.display_filtered_transactions(transactions)

    def clear_filter(self):
        self.load_transactions()

    def sort_by_date(self):
        date, ok = QInputDialog.getItem(self, 'Sort by Date', 'Select sorting order:', ['Ascending', 'Descending'], 0, False)
        if ok and date:
            if date == 'Ascending':
                transactions = sort_transaction_by_date_asc()
            else:
                transactions = sort_transaction_by_date_desc()
            self.display_filtered_transactions(transactions)

    def display_filtered_transactions(self, transactions):
        self.clear_transaction_cards()
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        for t in transactions.to_dict('records'):
            transaction_widget = self.create_transaction_card(t)
            self.scroll_layout.addWidget(transaction_widget)

    def load_transactions(self):
        transactions = read_transaction()
        transactions = transactions.sort_values('date', ascending=False)
        self.clear_transaction_cards()
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for t in transactions.to_dict('records'):
            transaction_widget = self.create_transaction_card(t)
            self.scroll_layout.addWidget(transaction_widget)

    def clear_transaction_cards(self):
        while self.scroll_layout.count() > 0:
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def create_transaction_card(self, transaction):
        card = QWidget()
        card_layout = QHBoxLayout(card)
        card.setStyleSheet("border: 1px solid gray; border-radius: 5px; padding: 2px;")

        # Bagian Kiri: Logo
        logo_label = QLabel()
        logo_label.setFixedSize(65, 65)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if transaction['type'] == 'expense':
            logo_label.setStyleSheet("background-color: #e80b67;")
        else:
            logo_label.setStyleSheet("background-color: #02b429;")
        category = transaction['category']
        logo_path = os.path.join(os.getcwd(), 'src', 'public', f'{category}.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap.scaled(65, 65, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_label.setText("No Logo")
        
        left_layout = QVBoxLayout()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(logo_label)

        category_label = QLabel(f"{transaction['category'].capitalize()}")
        if transaction['type'] == 'expense':
            category_label.setStyleSheet("font-size: 10px; font-weight: bold; margin-top: 2.5px; color: white; background-color: #e80b67;")
        else:
            category_label.setStyleSheet("font-size: 10px; font-weight: bold; margin-top: 2.5px; color: white; background-color: #02b429;")
        category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        category_label.setFixedWidth(65)  # Sesuaikan lebar teks dengan lebar logo
        left_layout.addWidget(category_label)

        card_layout.addLayout(left_layout)
        # Bagian Tengah: Amount dan Tombol
        center_layout = QVBoxLayout()
        # Amount
        amount_label = QLabel(f"Rp {transaction['amount']:,.2f}")
        if transaction['type'] == 'expense':
            amount_label.setStyleSheet("color: #D43A1C; font-weight: bold; font-size: 16px; border:none;")
        else:
            amount_label.setStyleSheet("color: #1CD43A; font-weight: bold; font-size: 16px; border:none;")

        center_layout.addWidget(amount_label)

        # Tombol Delete dan Edit
        button_layout = QHBoxLayout()
        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet("""
                                    QPushButton{
                                        background-color: #FF0000; 
                                        border:none; 
                                        color: white;
                                    }
                                    QPushButton:hover{
                                        background-color: #D43A1C;
                                    }
                                    """)
        delete_button.clicked.connect(lambda: self.confirm_delete_transaction(transaction['id']))
        edit_button = QPushButton("Edit")
        edit_button.setStyleSheet("""
                                  QPushButton{
                                    background-color: #0090FF;
                                    border:none;
                                    color: white;
                                  }
                                  QPushButton:hover{
                                    background-color: #0073e6;
                                  }
                                  """)
        edit_button.clicked.connect(lambda: self.edit_transaction(transaction['id']))
        button_layout.addWidget(delete_button)
        button_layout.addWidget(edit_button)
        center_layout.addLayout(button_layout)

        card_layout.addLayout(center_layout)

        # Bagian Kanan: Date
        date_label = QLabel(f"Date: {transaction['date']}")
        date_label.setStyleSheet("font-size: 30px; color: #0f0f0f; background-color: #f0f0f0; padding: 5px;border:none;")
        date_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        card_layout.addWidget(date_label)

        return card

    def delete_transaction(self, id):
        delete_transaction(id)
        self.load_transactions()

    def confirm_delete_transaction(self, id):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Konfirmasi")
        msg_box.setText("Apakah anda yakin untuk mendelete transaksi?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.delete_transaction(id)
            self.transaction_updated.emit()


    def edit_transaction(self, id):
        from views.update_transaction import TransactionFormEditUI
        self.edit_form = TransactionFormEditUI(self, id)
        self.edit_form.show()
        self.edit_form.closed.connect(self.load_transactions)
        self.transaction_updated.emit()
        self.budget_ui.refresh_ui()


    def open_create_form(self):
        from views.create_transaction import TransactionFormUI
        self.create_form = TransactionFormUI(self)
        self.create_form.show()
        self.create_form.closed.connect(self.load_transactions)
        self.transaction_updated.emit()
        self.budget_ui.refresh_ui()
    def refresh_budget_view(self):
        # Misalnya, panggil method untuk memuat ulang data budget
        self.budget_ui.refresh_ui()
# def metodo(self):
#     methods = ["Watershed", "Hough Circle"]
#     input_dialog = QInputDialog(self)
#     input_dialog.setWindowTitle("Choose Method")
#     input_dialog.setLabelText("Select counting method:")
#     input_dialog.setComboBoxItems(methods)
#     # Set a custom stylesheet for QInputDialog
#     input_dialog.setStyleSheet("color: black;")
#     method, ok = input_dialog.getItem(self, "Choose Method", "Select counting method:", methods, 0, False)
#     # after you close the white one,
#     # the correct dialog with black text should show up
#     input_dialog.show() 

#     if ok and method:
#         if method == "Watershed":
#             self.m = 'w'
#         elif method == "Hough Circle":
#             self.m = 'h'
#         self.counter()
#     else:
#         QMessageBox.information(self, "No Selection", "You didn't select a method.")
