 
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSpacerItem, QSizePolicy, QPushButton
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
import sys
import os

# Import controllers
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.views.components.navbar import Navbar
from src.controllers.userC import get_chart_data, create_pie_chart, get_financial_summary
import matplotlib.pyplot as plt

 

#------------------------------
class HomeUI(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id  # Simpan user_id sebagai properti kelas
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Add Navbar
        self.add_navbar(main_layout)

        # Balance Section
        self.add_balance_section(main_layout)

        # Pie Chart Section
        self.add_pie_chart_section(main_layout)

        # Transactions Section
        self.add_transactions_section(main_layout)

        # Spacer at the bottom
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def add_navbar(self, layout):
        navbar_layout = QHBoxLayout()
        
        # Buttons for the navbar
        buttons = {
            "Budget": "View and manage your budgets",
            "Home": "Go to home screen",
            "Transactions": "View your transactions"
        }

        for text, tooltip in buttons.items():
            btn = QPushButton(text)
            btn.setStyleSheet("font-size: 14px; padding: 8px; border: none;")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setToolTip(tooltip)
            navbar_layout.addWidget(btn)

        layout.addLayout(navbar_layout)

    def add_balance_section(self, layout):
        balance_layout = QVBoxLayout()

        # Get financial summary for the current user
        summary = get_financial_summary(self.user_id)

        balance_label = QLabel("Balance")
        balance_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Assuming the first row contains the latest balance
        if not summary.empty:
            latest_balance = summary.iloc[0]['amount']
            balance_amount = QLabel(f"Rp {latest_balance}")
        else:
            balance_amount = QLabel("Rp 0")

        balance_amount.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        balance_amount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        balance_subtext = QLabel("Latest Transaction Amount")
        balance_subtext.setFont(QFont("Arial", 10))
        balance_subtext.setAlignment(Qt.AlignmentFlag.AlignCenter)

        balance_layout.addWidget(balance_label)
        balance_layout.addWidget(balance_amount)
        balance_layout.addWidget(balance_subtext)
        layout.addLayout(balance_layout)

    def add_pie_chart_section(self, layout):
        data_group = get_chart_data(self.user_id)
        self.create_high_res_pie_chart(data_group)

        pie_chart_label = QLabel()
        chart_path = 'chart.png'

        if os.path.exists(chart_path):
            pixmap = QPixmap(chart_path)
            # Scale the image with smooth transformation
            pie_chart_label.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            pie_chart_label.setText("Pie chart unavailable")

        pie_chart_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(pie_chart_label)

        # Legend Section
        legend_layout = QHBoxLayout()
        for category, color in zip(data_group.index, ['#FFA500', '#008000', '#FF69B4', '#6495ED']):
            legend_item = QLabel(f"<span style='color:{color};'>●</span> {category}")
            legend_item.setFont(QFont("Arial", 10))
            legend_layout.addWidget(legend_item)
        layout.addLayout(legend_layout)

    def add_transactions_section(self, layout):
        transactions_label = QLabel("Most Recent Transactions")
        transactions_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(transactions_label)

        summary = get_financial_summary(self.user_id)

        if not summary.empty and {'type', 'amount', 'category'}.issubset(summary.columns):
            for _, row in summary.iterrows():
                self.add_transaction_item(
                    layout,
                    row['type'],
                    row['category'],
                    row['amount'],
                    "#008000" if row['amount'] > 0 else "#FF0000"
                )
        else:
            no_transaction_label = QLabel("No recent transactions available.")
            no_transaction_label.setFont(QFont("Arial", 10))
            layout.addWidget(no_transaction_label)

    def add_transaction_item(self, layout, transaction_type, category, amount, color):
        transaction_layout = QHBoxLayout()

        transaction_name = QLabel(transaction_type)
        transaction_name.setFont(QFont("Arial", 10))

        transaction_category = QLabel(category)
        transaction_category.setFont(QFont("Arial", 10))
        transaction_category.setStyleSheet("color: gray;")

        transaction_amount = QLabel(f"Rp {amount}")
        transaction_amount.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        transaction_amount.setStyleSheet(f"color: {color};")

        transaction_layout.addWidget(transaction_name)
        transaction_layout.addStretch()
        transaction_layout.addWidget(transaction_category)
        transaction_layout.addWidget(transaction_amount)
        layout.addLayout(transaction_layout)

    def create_high_res_pie_chart(self, data):
        # Delete old chart file if it exists
        chart_path = 'chart.png'
        if os.path.exists(chart_path):
            os.remove(chart_path)

        # Create high-resolution pie chart
        if not data.empty:
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(data, labels=data.index, autopct='%1.1f%%', colors=['#FFA500', '#008000', '#FF69B4', '#6495ED'])
            plt.savefig(chart_path, dpi=300)
            plt.close()

if __name__ == "__main__":
    from PyQt6.QtGui import QGuiApplication

    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    user_id = 1  # Ubah sesuai ID pengguna
    window = HomeUI(user_id)
    window.show()
    sys.exit(app.exec())
