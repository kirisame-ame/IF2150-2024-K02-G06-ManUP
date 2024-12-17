import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

def getBudgetAllocations():
    budget = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))
    return budget

def updateBudget(data):
    budget = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))
    budget.loc[budget['id'] == data['id'], 'budgetName'] = data['budgetName']
    budget.loc[budget['id'] == data['id'], 'budgetAmount'] = data['budgetAmount']
    budget.loc[budget['id'] == data['id'], 'remainder'] = data['remainder']
    budget.loc[budget['id'] == data['id'], 'startDate'] = data['startDate']
    budget.loc[budget['id'] == data['id'], 'endDate'] = data['endDate']
    budget.to_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'), index=False)

def createBudget(data):
    budget = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))
    budget = pd.concat([budget, pd.DataFrame([data])], ignore_index=True)
    budget.to_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'), index=False)

def getBudget(id):
    budget = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))
    budget = budget[budget['id'] == id]
    return budget

def deleteBudget(id):
    budget = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))
    budget = budget[budget['id'] != id]
    budget.to_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'), index=False)

def getBudgetByStartDate(date):
    budget = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))
    budget = budget[budget['startDate'] == date]
    return budget

def getBudgetByEndDate(date):
    budget = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))
    budget = budget[budget['endDate'] == date]
    return budget

def getBudgetByBudgetName(budgetName):
    budget = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))
    budget = budget[budget['budgetName'] == budgetName]
    return budget

def getBudgetByBudgetAmount(budgetAmount):
    budget = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))
    budget = budget[budget['budgetAmount'] == budgetAmount]
    return budget

def sortBudgetByBudgetAmount():
    budget = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))
    budget = budget.sort_values('budgetAmount')
    return budget

def sortBudgetByStartDate():
    budget = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))
    budget = budget.sort_values('startDate')
    return budget

def sortBudgetByEndDate():
    budget = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))
    budget = budget.sort_values('endDate')
    return budget

def getNewIdB():
    budget = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'budget.csv'))
    return budget['id'].max() + 1
