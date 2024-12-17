import sys
import os
import pandas as pd
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QLabel,
    QPushButton, QDialog, QLineEdit, QMessageBox, QFrame, QSpacerItem, QSizePolicy,
    QSplitter, QGraphicsDropShadowEffect, QProgressBar, 
)
from PyQt6.QtGui import QFont, QPixmap, QColor
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from controllers.budgetC import deleteBudget, updateBudget
from controllers.savingC import updateCurrentAmount, delete_saving, create_saving, read_savings, getTargetAmount, getCurrentAmount, getTargetDate, getStartDate
from views.components.navbar import Navbar


class BudgetUI(QWidget):
    def __init__(self):
        super().__init__()
        self.pie_chart = None
        self.scroll_area = None
        self.budget_layout = None  # Store the budget layout
        self.setup_ui()
        self.load_savings()

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
        self.savings_layout = QVBoxLayout(savings_section)
        splitter.addWidget(savings_section)

        title_layout = QHBoxLayout()
        title_layout.setSpacing(0)
        title_layout.setContentsMargins(0, 0, 0, 0)
        savings_label = QLabel("SAVINGS")
        savings_label.setStyleSheet("""
            color: #19191c;
            background-color: transparent; 
            padding-top: 5px;
            padding-right: 5px;
            text-align:
             center;
            """)
        font = QFont()
        font.setFamily("Helvetica")  # Menggunakan font Arial
        font.setPointSize(24)    # Ukuran font 24pt
        font.setWeight(QFont.Weight.Bold)  # Menggunakan font bold
        font.setItalic(False)
        font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 110)

        create_button = QPushButton("+")
        create_button.clicked.connect(lambda: self.create_saving_form())
        create_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: #29bd1e;  /* Warna oranye */
                color: white;
                border-radius: 9px;       /* Membuat tombol melengkung */
            }
            QPushButton:hover {
                background-color: #FF4500; /* Warna saat hover */
            }
        """)
        savings_label.setFont(font)
        savings_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        title_layout.addWidget(savings_label)
        title_layout.addWidget(create_button)
        title_layout.setAlignment(Qt.AlignmentFlag.AlignJustify)
        title_layout.setContentsMargins(0, 0, 0, 0)
        self.savings_layout.addLayout(title_layout)
        
        self.scroll_saving = QScrollArea()
        self.scroll_saving.setWidgetResizable(True)
        self.container = QWidget()
        self.containerSaving_layout = QVBoxLayout(self.container)
        self.containerSaving_layout.setSpacing(15)  # Tambahkan jarak antar elemen card
        self.containerSaving_layout.setContentsMargins(15, 15, 15, 15)  # Tambahkan margin untuk container
        
        self.scroll_saving.setWidget(self.container)
        self.savings_layout.addWidget(self.scroll_saving)

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


    def load_savings(self):
        savings = read_savings()
        self.clear_savings_cards()

        for s in savings.to_dict('records'):
            saving_widget = self.create_saving_card(self.containerSaving_layout, s)
            self.containerSaving_layout.addWidget(saving_widget, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    def clear_savings_cards(self):
        while self.containerSaving_layout.count() > 0:
            child = self.containerSaving_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def create_saving_card(self, container_layout, saving) -> QWidget:
        saving_id = saving['id']
        saving_target_date = getTargetDate(saving_id)
        saving_start_date = getStartDate(saving_id)
        saving_current_amount = getCurrentAmount(saving_id)
        saving_target_amount = getTargetAmount(saving_id)

        card = QWidget(self)
        card_layout = QVBoxLayout(card)
        card.setStyleSheet("""
            border: 0.5px solid #58595c;
            border-radius: 30px;
            padding: 1px;
            background-color: #FFFFFF;
        """)

        card.setFixedSize(600, 150) 
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(QColor(0, 0, 0, 60))  # Black with 60% transparency
        shadow_effect.setOffset(3, 5)
        card.setGraphicsEffect(shadow_effect)

        # Layout utama untuk widget card
        card_layout.setContentsMargins(30, 20, 30, 10)

        # Header Layout untuk judul dan target amount
        header_layout = QHBoxLayout()
        header_layout.setSpacing(0)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("Target Amount")
        title_label.setStyleSheet("""
            color: #404247;
            background-color: transparent;
            border: none;
            padding: 0px 0px 5px 0px; 
            text-align: left;
            """)
        title_label.setFont(QFont("Roboto", 18))
        header_layout.addWidget(title_label)

        self.amount_label = QLabel(f"{saving_target_amount:,.0f}")
        self.amount_label.setFont(QFont("Roboto", 18, QFont.Weight.Bold))
        self.amount_label.setStyleSheet("""
            color: #404247; 
            border: none;
            background-color: transparent; 
            padding: 0px 0px 0px 0px;
            text-align: left;
            """)  # Warna merah
        header_layout.addWidget(self.amount_label)
        header_layout.addStretch(0) 

        add_button = QPushButton("Add")
        add_button.clicked.connect(lambda: self.add_saving(saving_id))
        add_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: #29bd1e;  /* Warna oranye */
                color: white;
                padding: 5px;
                border-radius: 6px;       /* Membuat tombol melengkung */
            }
            QPushButton:hover {
                background-color: #FF4500; /* Warna saat hover */
            }
        """)
        header_layout.addWidget(add_button)
        card_layout.addLayout(header_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, saving_target_amount)
        self.progress_bar.setValue(saving_target_amount)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid black;
                border-radius: 10px;
                background-color: white;
                height: 20px;
            }
            QProgressBar::chunk {
                border-radius: 8px;
                background-color: #7ED957;
            }
        """)
        card_layout.addWidget(self.progress_bar)

        # Footer Layout untuk tanggal
        footer_layout = QHBoxLayout()
        start_label = QLabel(saving_start_date)
        start_label.setFont(QFont("Arial", 12))
        start_label.setStyleSheet("""color: #A9A9A9;
            background-color: transparent;
            border: none;
            padding: 0px 0px 2px 0px;
            text-align: left;
            """)
        footer_layout.addWidget(start_label)

        target_label = QLabel(saving_target_date)
        target_label.setFont(QFont("Arial", 12))
        target_label.setStyleSheet("""color: #A9A9A9;
            background-color: transparent; 
            border: none;
            padding: 0px 0px 2px 0px;
            text-align: right;
            """)
        footer_layout.addWidget(target_label)
        footer_layout.setStretch(0,1)

        card_layout.addLayout(footer_layout)

        center_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: #d12f19;  /* Warna oranye */
                color: white;
                padding: 5px;
                border-radius: 8px;       /* Membuat tombol melengkung */
            }
            QPushButton:hover {
                background-color: #5e150b; /* Warna saat hover */
            }
        """)

        # border: 0.5px solid #58595c;
        #     border-radius: 30px;
        #     padding: 1px;
        #     background-color: #FFFFFF;

        delete_button.clicked.connect(lambda: self.delete_saving(saving_id))
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda: self.edit_saving(saving_id))
        edit_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: #f28211;  /* Warna oranye */
                color: white;
                padding: 5px;
                border-radius: 8px;       /* Membuat tombol melengkung */
            }
            QPushButton:hover {
                background-color: #804f1f; /* Warna saat hover */
            }
        """)
        button_layout.addStretch(0)
        button_layout.addWidget(delete_button, alignment=Qt.AlignmentFlag.AlignRight)
        button_layout.addWidget(edit_button, alignment=Qt.AlignmentFlag.AlignRight)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        center_layout.addLayout(button_layout)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        card_layout.addLayout(center_layout)


        self.updateProgressManually(saving_current_amount, saving_target_amount)
        return card



    def updateProgressManually(self, current_amount, target_amount):
        """
        Perbarui progress bar secara manual dengan current_amount dan target_amount baru.
        """
        self.current_amount = current_amount
        self.target_amount = target_amount

        # Perbarui nilai progress bar
        self.progress_bar.setRange(0, self.target_amount)
        self.progress_bar.setValue(self.current_amount)

        # Perbarui teks target amount
        self.amount_label.setText(f"{self.target_amount:,.0f}")

        # Ubah warna progress bar berdasarkan persentase
        percentage = (self.current_amount / self.target_amount) * 100 if self.target_amount else 0
        if percentage > 80:
            color = "#FF6347"  # Merah
        elif percentage > 50:
            color = "#FFD700"  # Emas
        else:
            color = "#7ED957"  # Hijau

        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid black;
                border-radius: 10px;
                background-color: white;
                height: 20px;
            }}
            QProgressBar::chunk {{
                border-radius: 8px;
                background-color: {color};
            }}
        """)
        
    
    def delete_saving(self, id):
        delete_saving(id)
        self.load_savings()

    def create_saving_form(self):
        print("pppp")
        from views.createSaving import SavingFormUI
        self.create_form = SavingFormUI(self)
        self.create_form.show()
        self.create_form.closed.connect(self.load_savings)

    def edit_saving(self, id):
        from views.editUi_saving import EditSavingFormUI
        self.edit_form = EditSavingFormUI(self, id)
        self.edit_form.show()
        self.edit_form.closed.connect(self.load_savings)
    
    def add_saving(self, id):
        from views.update_saving import UpdateSavingFormUI
        self.edit_form = UpdateSavingFormUI(self, id)
        self.edit_form.show()
        self.edit_form.closed.connect(self.load_savings)
    # def edit_transaction(self, id):
    #     from views.update_transaction import TransactionFormEditUI
    #     self.edit_form = TransactionFormEditUI(self, id)
    #     self.edit_form.show()
    #     self.edit_form.closed.connect(self.load_transactions)

    # def open_create_form(self):
    #     from views.create_transaction import TransactionFormUI
    #     self.create_form = TransactionFormUI(self)
    #     self.create_form.show()
    #     self.create_form.closed.connect(self.load_transactions)


        # def create_saving_action(self):
    #     dialog = QInputDialog(self)
    #     dialog.setInputMode(QInputDialog.InputMode.TextInput)
    #     dialog.setWindowTitle("Create Saving")
    #     dialog.setLabelText("Enter new saving data (id,targetAmount,startDate,targetDate,currentAmount):")
    #     if dialog.exec() == QInputDialog.DialogCode.Accepted:
    #         data = dialog.textValue()
    #         try:
    #             id, targetAmount, startDate, targetDate, currentAmount = data.split(',')
    #             create_saving({
    #                 'id': int(id),
    #                 'targetAmount': int(targetAmount),
    #                 'startDate': startDate,
    #                 'targetDate': targetDate,
    #                 'currentAmount': int(currentAmount),
    #             })
    #             QMessageBox.information(self, "Success", "Saving created successfully!")
    #         except Exception as e:
    #             QMessageBox.critical(self, "Error", f"Failed to create saving: {e}")

    # def add_saving_action(self):
    #     dialog = QInputDialog(self)
    #     dialog.setInputMode(QInputDialog.InputMode.TextInput)
    #     dialog.setWindowTitle("Add Saving")
    #     dialog.setLabelText("Enter id and amount to add (id,amount):")
    #     if dialog.exec() == QInputDialog.DialogCode.Accepted:
    #         data = dialog.textValue()
    #         try:
    #             id, amount = map(int, data.split(','))
    #             updateCurrentAmount(id, amount)
    #             QMessageBox.information(self, "Success", "Amount added successfully!")
    #         except Exception as e:
    #             QMessageBox.critical(self, "Error", f"Failed to add amount: {e}")

    # def delete_saving_action(self):
    #     dialog = QInputDialog(self)
    #     dialog.setInputMode(QInputDialog.InputMode.TextInput)
    #     dialog.setWindowTitle("Delete Saving")
    #     dialog.setLabelText("Enter id to delete:")
    #     if dialog.exec() == QInputDialog.DialogCode.Accepted:
    #         try:
    #             id = int(dialog.textValue())
    #             delete_saving(id)
    #             QMessageBox.information(self, "Success", "Saving deleted successfully!")
    #         except Exception as e:
    #             QMessageBox.critical(self, "Error", f"Failed to delete saving: {e}")