import pandas as pd
import sys
import os

import matplotlib.pyplot as plt

def simplify_data(data_group, threshold=0.05):
    small_categories = data_group[data_group / data_group.sum() < threshold].index
    data_group.loc['Lain-lain'] = data_group.loc[small_categories].sum()
    data_group = data_group.drop(small_categories)
    return data_group

def get_financial_summary(id):
    transaction = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'transaction.csv'))
    filter_transaction = transaction[transaction['id'] == id]
    sorted_transaction = filter_transaction.sort_values(by='amount', ascending=False)
    top3_summary = sorted_transaction.head(3)
    return top3_summary
    
def get_chart_data(user_id):
    # Baca data transaksi
    transaction = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'transaction.csv'))
    
    # Filter transaksi berdasarkan id pengguna
    filtered_transactions = transaction[transaction['id'] == user_id]
    filtered_transactions = transaction[(transaction['id'] == user_id) & (transaction['type'] == 'expense')]
    
    # Grup data berdasarkan 'type' dan hitung total 'amount'
    data_group = filtered_transactions.groupby('category')['amount'].sum()
    
    return data_group


def create_pie_chart(data_group, output_file='chart.png'):
    plt.figure(figsize=(8, 8))
    colors = ['#FFA500', '#008000', '#FF69B4', '#6495ED', '#FF4500']  # Contoh warna
    data_group.plot.pie(autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('Distribusi Tipe Transaksi')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()

def get_notifications():
    # Contoh data notifikasi
    return ["You have a new message.", "Your budget is running low!"]

# def get_user_details(user_id):
#     # Mengambil data user berdasarkan ID
#     return User.get_user_by_id(user_id)