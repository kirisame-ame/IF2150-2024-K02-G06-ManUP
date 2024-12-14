import sys
import os
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QLabel,
    QPushButton, QDialog, QLineEdit, QMessageBox, QFrame, QSpacerItem, QSizePolicy,
    QSplitter
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from views.components.navbar import Navbar
from controllers.budgetC import deleteBudget, updateBudget

from PyQt6.QtCore import pyqtSignal
class BudgetUI(QWidget):
    budget_updated = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.pie_chart = None
        self.scroll_area = None
        self.budget_layout = None  # Store the budget layout
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)

        # Add navbar
        self.navbar = Navbar()
        main_layout.addWidget(self.navbar)

        # Splitter for proportional layout
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Savings section
        savings_section = QFrame()
        savings_layout = QVBoxLayout(savings_section)
        savings_label = QLabel("Savings")
        savings_label.setStyleSheet("font-size: 18px; font-weight: bold; text-align: center;")
        savings_amount = QLabel("$5000")  # Example value
        savings_amount.setStyleSheet("font-size: 24px; color: green; text-align: center;")
        savings_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        savings_layout.addWidget(savings_label, alignment=Qt.AlignmentFlag.AlignCenter)
        savings_layout.addWidget(savings_amount, alignment=Qt.AlignmentFlag.AlignCenter)
        savings_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        splitter.addWidget(savings_section)

        # Budget section
        budget_section = QFrame()
        self.budget_layout = QVBoxLayout(budget_section)  # Assign to instance variable
        splitter.addWidget(budget_section)

        # Path to the CSV file
        csv_path = os.path.join(os.getcwd(), 'src', 'models', 'budget.csv')

        # Add pie chart
        self.pie_chart = self.create_pie_chart(csv_path)
        self.budget_layout.addWidget(self.pie_chart, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add scrollable table
        self.scroll_area = self.create_scrollable_cards(csv_path)
        self.budget_layout.addWidget(self.scroll_area)

        # Add splitter to the main layout
        splitter.setSizes([250, 250])
        main_layout.addWidget(splitter)

        # Set styling
        self.setStyleSheet(
            """
            QLabel {
                text-align: center;
            }
            QTableWidget {
                gridline-color: #d3d3d3;
                font-size: 14px;
            }
            QPushButton {
                font-size: 12px;
                padding: 5px;
            }
            """
        )

    def create_pie_chart(self, csv_file):
        # Read data from CSV
        data = pd.read_csv(csv_file)
        labels = data['budgetName']
        amounts = data['budgetAmount']

        # Create a matplotlib figure and axis with transparent background
        figure, ax = plt.subplots(figsize=(5, 5), tight_layout=True)
        figure.patch.set_alpha(0.0)  # Make the figure background transparent
        ax.set_facecolor('none')      # Make the axes background transparent

        # Define colors for the pie chart
        colors = plt.cm.Set3(range(len(labels)))

        # Define a function to show percentages only for non-zero values
        def autopct_func(pct):
            return f"{pct:.1f}%" if pct > 0 else ""

        # Create the pie chart
        wedges, texts, autotexts = ax.pie(
            amounts,
            labels=[label if amount > 0 else '' for label, amount in zip(labels, amounts)],
            autopct=autopct_func,
            startangle=140,
            colors=colors,
            wedgeprops={'edgecolor': 'w', 'linewidth': 1.5},
            textprops={'fontsize': 8, 'weight': 'bold'},
            pctdistance=0.75,
        )

        # Add a transparent center circle for a donut chart effect
        center_circle = plt.Circle((0, 0), 0.5, color='white', fc='white', linewidth=0)
        ax.add_artist(center_circle)

        # Create the FigureCanvas and set its background to transparent
        canvas = FigureCanvas(figure)
        canvas.setStyleSheet("background: transparent;")

        return canvas


    def create_scrollable_cards(self, csv_file):
        data = pd.read_csv(csv_file)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout(container)

        for i, row in data.iterrows():
            card = QWidget()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(30, 30, 30, 30)
            card_layout.setSpacing(10)
            card.setStyleSheet(
                """
                border-radius: 10px;
                border: 2px solid #d3d3d3;
                """
            )

            budget_name = row.get('budgetName', '')
            title_label = QLabel(budget_name)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setStyleSheet(
                """
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    background-color: #4caf50;
                    color: white;
                    padding: 10px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }
                """
            )
            card_layout.addWidget(title_label)

            amount_and_remainder_layout = QHBoxLayout()
            budget_amount_label = QLabel(f"Amount: {row.get('budgetAmount', 'N/A')}")
            budget_amount_label.setStyleSheet(
                """
                QLabel {
                    font-size: 20px;
                    font-weight: bold;
                    color: #333;
                    padding: 5px 30px;
                    border-radius: 10px;
                    border: 1px solid #d3d3d3;
                }
                """
            )
            amount_and_remainder_layout.addWidget(budget_amount_label)

            remainder_label = QLabel(f"Remainder: {row.get('remainder', 'N/A')}")
            remainder_label.setStyleSheet(
                """
                QLabel {
                    font-size: 20px;
                    color: white;
                    background-color: #f44336;
                    padding: 5px 30px;
                    border-radius: 10px;
                    border: 1px solid #d3d3d3;
                }
                """
            )
            amount_and_remainder_layout.addWidget(remainder_label)

            card_layout.addLayout(amount_and_remainder_layout)

            start_date = row.get('startDate', 'N/A')
            end_date = row.get('endDate', 'N/A')
            timeline_label = QLabel(f"{start_date} - {end_date}")
            timeline_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            timeline_label.setStyleSheet(
                """
                QLabel {
                    font-size: 20px;
                    color: #555;
                    padding: 5px 30px;
                    margin-top: 10px;
                    margin-bottom: 10px;
                    font-weight: bold;
                    border: 1px solid #d3d3d3;
                    border-radius: 10px;
                }
                """
            )
            card_layout.addWidget(timeline_label)

            button_layout = QHBoxLayout()
            button_layout.setContentsMargins(10, 10, 10, 10)

            edit_button = QPushButton("Edit")
            edit_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 4px;
                    font-size: 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976d2;
                }
                """
            )
            edit_button.clicked.connect(lambda _, r=row: self.show_edit_popup(r))
            button_layout.addWidget(edit_button)

            # delete_button = QPushButton("Delete")
            # delete_button.setStyleSheet(
            #     """
            #     QPushButton {
            #         background-color: #f44336;
            #         color: white;
            #         border: none;
            #         padding: 10px 20px;
            #         border-radius: 4px;
            #         font-size: 20px;
            #         font-weight: bold;
            #     }
            #     QPushButton:hover {
            #         background-color: #d32f2f;
            #     }
            #     """
            # )
            # delete_button.clicked.connect(lambda _, r=row: self.confirm_delete(r))
            # button_layout.addWidget(delete_button)

            card_layout.addLayout(button_layout)
            container_layout.addWidget(card)

        scroll_area.setWidget(container)
        return scroll_area

    def show_edit_popup(self, row):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Budget")
        dialog.setStyleSheet(
            """
            QDialog {
                background-color: #f9f9f9;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                font-size: 16px;
                color: #333;
                margin-bottom: 5px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-bottom: 15px;
            }
            QPushButton {
                font-size: 14px;
                background-color: #4caf50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            """
        )

        dialog_layout = QVBoxLayout(dialog)

        # Input fields with labels
        fields = {
            "Budget Name": QLineEdit(row.get('budgetName', '')),
            "Budget Amount": QLineEdit(str(row.get('budgetAmount', ''))),
            "Remainder": QLineEdit(str(row.get('remainder', ''))),
            "Start Date (YYYY-MM-DD)": QLineEdit(row.get('startDate', '')),
            "End Date (YYYY-MM-DD)": QLineEdit(row.get('endDate', '')),
        }

        # Add labeled input fields to the dialog
        for label_text, input_field in fields.items():
            label = QLabel(label_text)
            dialog_layout.addWidget(label)
            dialog_layout.addWidget(input_field)

        # Save button
        save_button = QPushButton("Save")
        save_button.setStyleSheet(
            """
            QPushButton {
                font-size: 14px;
                background-color: #2196f3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            """
        )
        save_button.clicked.connect(
            lambda: self.save_edit(
                row,
                fields["Budget Name"],
                fields["Budget Amount"],
                fields["Remainder"],
                fields["Start Date (YYYY-MM-DD)"],
                fields["End Date (YYYY-MM-DD)"],
                dialog
            )
        )
        dialog_layout.addWidget(save_button)

        dialog.exec()




    def save_edit(self, row, name_input, amount_input, remainder_input, start_date_input, end_date_input, dialog):
        try:
            updated_data = {
                'id': row['id'],
                'budgetName': name_input.text(),
                'budgetAmount': float(amount_input.text()),
                'remainder': float(remainder_input.text()),
                'startDate': start_date_input.text(),
                'endDate': end_date_input.text()
            }
            updateBudget(updated_data)  # Update the budget data
            self.refresh_ui()  # Refresh the UI to reflect changes
            self.budget_updated.emit()  # Emit signal to update the budget in the main window
            dialog.close()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please ensure all fields are correctly filled.")



    def confirm_delete(self, row):
        reply = QMessageBox.question(
            self, "Confirm Delete", f"Are you sure you want to delete {row['budgetName']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            deleteBudget(row['id'])
            self.refresh_ui()

    def refresh_ui(self):
        csv_path = os.path.join(os.getcwd(), 'src', 'models', 'budget.csv')

        # Replace the pie chart
        if self.pie_chart:
            self.budget_layout.removeWidget(self.pie_chart)
            self.pie_chart.deleteLater()
            self.pie_chart = None

        self.pie_chart = self.create_pie_chart(csv_path)
        self.budget_layout.addWidget(self.pie_chart, alignment=Qt.AlignmentFlag.AlignCenter)

        # Replace the scroll area
        if self.scroll_area:
            self.budget_layout.removeWidget(self.scroll_area)
            self.scroll_area.deleteLater()
            self.scroll_area = None

        self.scroll_area = self.create_scrollable_cards(csv_path)
        self.budget_layout.addWidget(self.scroll_area)
