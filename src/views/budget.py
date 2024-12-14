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

        # savings_label = QLabel("SAVINGS")
        # savings_label.setStyleSheet("""
        #     color: #19191c;
        #     background-color: transparent; 
        #     padding-top: 5px;
        #     text-align: center;
        #     """)
        # font = QFont()
        # font.setFamily("Helvetica")  # Menggunakan font Arial
        # font.setPointSize(24)    # Ukuran font 24pt
        # font.setWeight(QFont.Weight.Bold)  # Menggunakan font bold
        # font.setItalic(False)
        # font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 110)
        # savings_label.setFont(font)
        # savings_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        # self.savings_layout.addWidget(savings_label)
        
        saving_data = read_savings()  # Ambil data saving (bisa berupa dictionary atau None)
        self.create_saving_view(saving_data)
        # savings_label = QLabel("Savings")
        # savings_label.setStyleSheet("font-size: 18px; font-weight: bold; text-align: center;")
        # savings_amount = QLabel("$5000")  # Example value
        # savings_amount.setStyleSheet("font-size: 24px; color: green; text-align: center;")
        # savings_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        # savings_layout.addWidget(savings_amount, alignment=Qt.AlignmentFlag.AlignCenter)
        # savings_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        #splitter.addWidget(savings_section)


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
        csv_pathSaving = os.path.join(os.getcwd(), 'src', 'models', 'savings.csv')

        # Replace the pie chart
        if self.savings_layout:
            self.removeWidget(self.savings_layout)
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


    def create_saving_view(self, saving):
        self.clear_savings_layout()

        # Jika tidak ada saving
        if saving is None or saving.empty:
            print("kosong cik")
            empty_label = QLabel("Tidak ada saving yang berjalan.")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("""
                color: #A9A9A9;
                font-size: 18px;
                font-style: italic;
            """)
            self.savings_layout.addWidget(empty_label)
        else:

            # Ambil data saving
            saving_id = saving['id'].iloc[0]
            saving_target_date = saving['targetDate'].iloc[0]
            saving_start_date = saving['startDate'].iloc[0]
            saving_current_amount = saving['currentAmount'].iloc[0]
            saving_target_amount = saving['targetAmount'].iloc[0]

            # Layout Utama
            main_layout = QVBoxLayout()
            main_layout.setContentsMargins(0, 10, 0, 10)  # Kurangi jarak atas dan bawah
            main_layout.setSpacing(20)  # Tambahkan jarak antar elemen

            # Header (Target Amount)
            header_layout = QHBoxLayout()
            target_label = QLabel("Target Amount")
            target_label.setStyleSheet("""
                color: #19191c;
                font-size: 20px;
                font-weight: bold;
            """)
            target_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            target_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed) 
            amount_label = QLabel(f"{saving_target_amount:,.0f}")
            amount_label.setStyleSheet("""
                color: #4CAF50;
                font-size: 20px;
                font-weight: bold;
            """)
            # background-color: transparent; 
            amount_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
            amount_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)

            header_layout.addWidget(target_label)
            header_layout.addWidget(amount_label)
            header_layout.setAlignment(Qt.AlignmentFlag.AlignJustify | Qt.AlignmentFlag.AlignTop)
            main_layout.addLayout(header_layout)

            # Progress Area Layout
            progress_area_layout = QHBoxLayout()

            # Bar Tanggal (Vertikal)
            date_bar_layout = QVBoxLayout()
            start_date_label = QLabel(saving_start_date)
            start_date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            start_date_label.setStyleSheet("""
                color: #A9A9A9;
                font-size: 14px;
            """)
            start_date_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
            end_date_label = QLabel(saving_target_date)
            end_date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            end_date_label.setStyleSheet("""
                color: #A9A9A9;
                font-size: 14px;
            """)
            end_date_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
            date_progress = QProgressBar()
            date_progress.setOrientation(Qt.Orientation.Vertical)
            date_progress.setRange(0, 100)
            date_progress.setValue(70)  # Placeholder untuk progress tanggal
            date_progress.setTextVisible(False)
            date_progress.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    background-color: #ffffff;
                    width: 20px;
                }
                QProgressBar::chunk {
                    background-color: #FF6347;
                }
            """)
            date_progress.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            date_progress.setMinimumHeight(550)
            
            date_bar_layout.addWidget(end_date_label, alignment=Qt.AlignmentFlag.AlignTop)
            date_bar_layout.addWidget(date_progress, alignment=Qt.AlignmentFlag.AlignCenter)
            date_bar_layout.addWidget(start_date_label, alignment=Qt.AlignmentFlag.AlignBottom)
            progress_area_layout.addLayout(date_bar_layout)

            # Area Progress Amount
            progress_frame = QFrame()
            progress_frame.setStyleSheet("""
                background-color: #f0f4f8;
                border-radius: 10px;
            """)
            progress_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Memungkinkan meluas
            progress_layout = QVBoxLayout(progress_frame)
            progress_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Semua elemen dirapatkan ke atas

            # Label "Current Amount"
            progress_label = QLabel("Current Amount")
            progress_label.setStyleSheet("""
                color: #A9A9A9;
                font-size: 16px;
            """)
            progress_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            progress_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
            progress_layout.addWidget(progress_label, alignment=Qt.AlignmentFlag.AlignTop)

            # Label Amount
            current_amount_label = QLabel(f"{saving_current_amount:,.0f}")
            current_amount_label.setStyleSheet("""
                color: #ffffff;
                font-size: 28px;
                font-weight: bold;
            """)
            current_amount_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            current_amount_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
            progress_layout.addWidget(current_amount_label, alignment=Qt.AlignmentFlag.AlignTop)

            # Progress Bar Vertikal
            progress_bar = QProgressBar()
            progress_bar.setOrientation(Qt.Orientation.Vertical)  # Progress bar vertikal
            progress_bar.setRange(0, saving_target_amount)
            progress_bar.setValue(saving_current_amount)
            progress_bar.setTextVisible(False)
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    background-color: #ffffff;
                    width: 40px;  /* Lebar progress bar */
                }
                QProgressBar::chunk {
                    border-radius: 10px;
                    background-color: #7ED957;
                }
            """)
            progress_bar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)  # Meluas vertikal
            progress_bar.setMinimumHeight(550)
            progress_bar.setMinimumWidth(400)
            progress_layout.addWidget(progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)

            # Tambahkan ke progress area
            progress_area_layout.addWidget(progress_frame)
            main_layout.addLayout(progress_area_layout, stretch=1)

            button_layout = QHBoxLayout()

        edit_button = QPushButton("Edit")
        edit_button.setStyleSheet("""
            background-color: #2196f3;
            color: #ffffff;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 10px;
        """)
        edit_button.clicked.connect(lambda: self.edit_saving(saving_id))  # Hubungkan ke fungsi edit
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet("""
            background-color: #FF6347;
            color: #ffffff;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 10px;
        """)
        delete_button.clicked.connect(lambda: self.delete_savings(saving_id))  # Hubungkan ke fungsi delete
        button_layout.addWidget(delete_button)

        main_layout.addLayout(button_layout)  # Tambahkan tombol ke layout utama

        # Tambahkan ke savings_layout
        self.savings_layout.addLayout(main_layout)
            

    def clear_savings_layout(self):
        print(str(self.savings_layout.count()))
        while self.savings_layout.count():
            item = self.savings_layout.takeAt(0)
            widget = item.widget()
            if widget:
                print(f"Hapus widget: {widget}") 
                widget.deleteLater()

    def delete_savings(self, saving_id):
        """
        Hapus data saving dari sumber data dan perbarui tampilan.
        """
        # Hapus data saving dari sumber data
        delete_saving(saving_id)

        # Bersihkan semua widget di layout savings
        self.savings_layout.removeWidget(self.savings_layout)
        self.sa
        while self.savings_layout.count():
            item = self.savings_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        # Tampilkan label kosong jika tidak ada saving
        empty_label = QLabel("Tidak ada saving yang berjalan.")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_label.setStyleSheet("""
            color: #A9A9A9;
            font-size: 18px;
            font-style: italic;
        """)
        self.savings_layout.addWidget(empty_label)
    def edit_saving(self, saving_id):
        from views.update_saving import SavingFormEditUI  # Pastikan Anda memiliki file ini
        self.edit_form = SavingFormEditUI(self, saving_id)
        self.edit_form.show()
        self.edit_form.closed.connect(self.refresh_ui)
    
        

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