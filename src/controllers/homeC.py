import pandas as pd
import sys
import os

import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
from controllers.budgetC import getBudgetAllocations
from controllers.transactionC import read_transaction
def get_four_most_recent_transaction():
    data = read_transaction()
    data = data.sort_values('date', ascending=False).head(4)
    return data.to_dict(orient='records')


def remainder():
    data = read_transaction()
    income = data[data['type'] == 'income']['amount'].sum()
    expense = data[data['type'] == 'expense']['amount'].sum()
    total_budget = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))['budgetAmount'].sum()
    remainder = total_budget + income - expense
    return remainder

def pie_chart_for_category_in_type_expense():
    budget_data = getBudgetAllocations()
    budget_amount = budget_data['budgetAmount']
    budget_names = budget_data['budgetName']
    budget_amount.index = budget_names

    # Append the remainder to pie chart
    remainder_ = remainder()
    budget_amount = pd.concat([budget_amount, pd.Series(remainder_, index=['Remainder'])])

    # Create a matplotlib figure and axis with transparent background
    figure, ax = plt.subplots(figsize=(5, 5), tight_layout=True)
    figure.patch.set_alpha(0.0)  # Make the figure background transparent
    ax.set_facecolor('none')      # Make the axes background transparent

    # Define colors for the pie chart
    colors = plt.cm.Set3(range(len(budget_amount)))

    # Define a function to show percentages only for non-zero values
    def autopct_func(pct):
        return f"{pct:.1f}%" if pct > 0 else ""

    # Create the pie chart
    wedges, texts, autotexts = ax.pie(
        budget_amount,
        labels=[label.capitalize() if amount > 0 else '' for label, amount in zip(budget_amount.index, budget_amount)],
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

    # Save the figure with a transparent background
    return figure

