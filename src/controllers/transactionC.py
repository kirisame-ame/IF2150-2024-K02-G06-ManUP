import pandas as pd



def read_transaction():
    transaction = pd.read_csv('models/transaction.csv')
    return transaction

def create_transaction(data):
    transaction = pd.read_csv('models/transaction.csv')
    transaction = transaction.append(data, ignore_index=True)
    transaction.to_csv('models/transaction.csv', index=False)
    return transaction

def delete_transaction(id):
    transaction = pd.read_csv('models/transaction.csv')
    transaction = transaction[transaction['id'] != id]
    transaction.to_csv('models/transaction.csv', index=False)
    return transaction

def update_transaction(data):
    transaction = pd.read_csv('models/transaction.csv')
    transaction = transaction[transaction['id'] != data['id']]
    transaction = transaction.append(data, ignore_index=True)
    transaction.to_csv('models/transaction.csv', index=False)
    return transaction

def get_transaction(id):
    transaction = pd.read_csv('models/transaction.csv')
    transaction = transaction[transaction['id'] == id]
    return transaction

def total_transaction():
    transaction = pd.read_csv('models/transaction.csv')
    income = transaction[transaction['type'] == 'income']['amount'].sum()
    expense = transaction[transaction['type'] == 'expense']['amount'].sum()
    total = income - expense
    return total

def get_transaction_by_type(type):
    transaction = pd.read_csv('models/transaction.csv')
    transaction = transaction[transaction['type'] == type]
    return transaction

def get_transaction_by_description(description):
    transaction = pd.read_csv('models/transaction.csv')
    transaction = transaction[transaction['description'] == description]
    return transaction

def get_transaction_by_date(date):
    transaction = pd.read_csv('models/transaction.csv')
    transaction = transaction[transaction['date'] == date]
    return transaction

def sort_transaction_by_date():
    transaction = pd.read_csv('models/transaction.csv')
    transaction = transaction.sort_values('date')
    return transaction