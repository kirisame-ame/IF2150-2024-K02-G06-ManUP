import sys
import os
import pandas as pd
import textwrap
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QSpacerItem,
    QSizePolicy,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QSplitter,
    QAbstractItemView,
    QHeaderView
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from views.components.navbar import Navbar
from controllers.budgetC import deleteBudget, updateBudget


class BudgetUI(QWidget):
    def __init__(self):
        super().__init__()
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
        # Center contents of the savings layout
        savings_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        savings_layout.addWidget(savings_label, alignment=Qt.AlignmentFlag.AlignCenter)
        savings_layout.addWidget(savings_amount, alignment=Qt.AlignmentFlag.AlignCenter)
        savings_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        splitter.addWidget(savings_section)

        # Budget section
        budget_section = QFrame()
        budget_layout = QVBoxLayout(budget_section)
        budget_label = QLabel("")
        budget_label.setStyleSheet("font-size: 18px; font-weight: bold; text-align: center;")
        budget_layout.addWidget(budget_label, alignment=Qt.AlignmentFlag.AlignCenter)
        splitter.addWidget(budget_section)

        csv_path = os.path.join(os.getcwd(), 'src', 'models', 'budget.csv')

        # Add pie chart
        pie_chart = self.create_pie_chart(csv_path)
        budget_layout.addWidget(pie_chart, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add scrollable table
        scroll_area = self.create_scrollable_cards(csv_path)
        budget_layout.addWidget(scroll_area)

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
        # Load CSV data
        data = pd.read_csv(csv_file)
        labels = data['budgetName']
        amounts = data['budgetAmount']

        # Matplotlib figure with modernized styling
        figure, ax = plt.subplots(figsize=(6, 6), tight_layout=True)
        figure.patch.set_alpha(0)  # Transparent figure background
        ax.set_facecolor('none')  # Transparent axes background
        colors = plt.cm.Set3(range(len(labels)))  # Modern color palette

        wedges, texts, autotexts = ax.pie(
            amounts,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            colors=colors,
            wedgeprops={'edgecolor': 'w', 'linewidth': 1.5},  # Clean wedge edges
            textprops={'fontsize': 10, 'weight': 'bold'},    # Modern label styling
            pctdistance=0.85,  # Position percentages closer to the center
        )

        # Add a white circle to create a donut chart effect
        ax.add_artist(plt.Circle((0, 0), 0.7, color='white', fc='white'))

        # Create a FigureCanvas for embedding in PyQt
        canvas = FigureCanvas(figure)
        return canvas

    def create_scrollable_table(self, csv_file):
        # Load CSV data
        data = pd.read_csv(csv_file)

        # Create a scrollable widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout(container)

        # Add a table for detailed data
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(data.columns) + 2)  # Extra columns for buttons
        table.setHorizontalHeaderLabels(list(data.columns) + ["Edit", "Delete"])

        # Populate the table with data and buttons
        for i, row in data.iterrows():
            for j, value in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(value)))

            # Add Edit button
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, r=i: self.edit_row(r))
            table.setCellWidget(i, len(data.columns), edit_button)

            # Add Delete button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, r=i: self.delete_row(r))
            table.setCellWidget(i, len(data.columns) + 1, delete_button)

        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # Disable direct editing

        # Stretch the table to fill the layout
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        container_layout.addWidget(table)
        scroll_area.setWidget(container)
        return scroll_area

    def create_scrollable_cards(self, csv_file):
        # Load CSV data
        data = pd.read_csv(csv_file)

        # Create a scrollable widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout(container)

        # Loop through each row to create a card
        for i, row in data.iterrows():
            # Create a card widget
            card = QWidget()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)  # Increased padding
            card_layout.setSpacing(15)

            # Add the budget name as a title at the top of the card
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

            # Display budgetAmount and remainder side by side
            amount_and_remainder_layout = QHBoxLayout()

            budget_amount_label = QLabel(f"Amount: {row.get('budgetAmount', 'N/A')}")
            budget_amount_label.setStyleSheet(
                """
                QLabel {
                    font-size: 14px;
                    color: #333;
                    padding: 5px 30px;
                }
                """
            )
            amount_and_remainder_layout.addWidget(budget_amount_label)

            remainder_label = QLabel(f"Remainder: {row.get('remainder', 'N/A')}")
            remainder_label.setStyleSheet(
                """
                QLabel {
                    font-size: 14px;
                    color: white;
                    background-color: #f44336;
                    padding: 5px 30px;
                    border-radius: 4px;
                }
                """
            )
            amount_and_remainder_layout.addWidget(remainder_label)

            card_layout.addLayout(amount_and_remainder_layout)

            # Add a timeline indicating startDate - endDate
            start_date = row.get('startDate', 'N/A')
            end_date = row.get('endDate', 'N/A')
            timeline_label = QLabel(f"{start_date} - {end_date}")
            timeline_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            timeline_label.setStyleSheet(
                """
                QLabel {
                    font-size: 14px;
                    color: #555;
                    padding: 5px 30px;
                    margin-top: 10px;
                    margin-bottom: 10px;
                    font-weight: bold;
                }
                """
            )
            card_layout.addWidget(timeline_label)

            # Create a button layout
            button_layout = QHBoxLayout()
            button_layout.setContentsMargins(10, 10, 10, 10)  # Added padding for buttons

            # Add Edit button
            edit_button = QPushButton("Edit")
            edit_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #2196f3;
                    color: white;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #1976d2;
                }
                """
            )
            edit_button.clicked.connect(lambda _, r=i: self.edit_row(r))
            button_layout.addWidget(edit_button)

            # Add Delete button
            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
                """
            )
            delete_button.clicked.connect(lambda _, r=i: self.delete_row(r))
            button_layout.addWidget(delete_button)

            # Add buttons to the card layout
            card_layout.addLayout(button_layout)

            # Style the card with a modernized look
            card.setStyleSheet(
                """
                QWidget {
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    background-color: #ffffff;
                    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
                }
                """
            )

            # Add the card to the container layout
            container_layout.addWidget(card)

        # Add some spacing between cards
        container_layout.addStretch()

        # Set the container to the scroll area
        scroll_area.setWidget(container)
        return scroll_area





    def edit_row(self, row):
        print(f"Edit row: {row}")
        # Logic for editing the row

    def delete_row(self, row):
        print(f"Delete row: {row}")
        # Logic for deleting the row
