import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

# id,targetAmount,startDate,targetDate,currentAmount
def getSavingsbyId(id: int) -> pd.DataFrame:
    savingDF = read_savings()
    saving = savingDF[savingDF['id'] == id]
    return saving

def getTargetAmount(id: int) -> int:
    saving = getSavingsbyId(id)
    targetAmount = int(saving['targetAmount'].values[0])
    return targetAmount

def getCurrentAmount(id: int) -> int:
    saving = getSavingsbyId(id)
    currentAmount = int(saving['currentAmount'].values[0])
    return currentAmount

def getStartDate(id: int) -> str:  
    saving = getSavingsbyId(id)    
    #startDate = savingDF.loc[savingDF['id'] == id, 'startDate'].values[0]
    startDate = saving['startDate'].values[0]
    return startDate

def getTargetDate(id: int) -> str:
    saving = getSavingsbyId(id)
    targetDate = saving['targetDate'].values[0]
    return targetDate

def setTargetAmount(id: int, newTargetAmount: int):
    savingDF = read_savings()
    savingDF.loc[savingDF['id'] == id, 'targetAmount'] = newTargetAmount
    savingDF.to_csv(os.path.join(os.getcwd(), 'src', 'models', 'saving.csv'), index=False)
    return

def setTargetDate(id: int, newTargetDate: str):
    savingDF = read_savings()
    savingDF.loc[savingDF['id'] == id, 'targetDate'] = newTargetDate
    savingDF.to_csv(os.path.join(os.getcwd(), 'src', 'models', 'saving.csv'), index=False)
    return

def updateCurrentAmount(id: int, amount: str):
    savingDF = read_savings()
    newAmount = getCurrentAmount(id) + amount
    savingDF.loc[savingDF['id'] == id, 'currentAmount'] = newAmount
    savingDF.to_csv(os.path.join(os.getcwd(), 'src', 'models', 'saving.csv'), index=False)
    return

def read_savings() -> pd.DataFrame:
    savings = pd.read_csv(os.path.join(os.getcwd(), 'src', 'models', 'saving.csv'))
    return savings

def create_saving(data):
    savingDF = read_savings()
    savingDF = pd.concat([savingDF, pd.DataFrame([data])], ignore_index=True)
    savingDF.to_csv(os.path.join(os.getcwd(), 'src', 'models', 'saving.csv'), index=False)

def delete_saving(id):
    savingDF = read_savings()
    savingDF = savingDF[savingDF['id'] != id]
    savingDF.to_csv(os.path.join(os.getcwd(), 'src', 'models', 'saving.csv'), index=False)

def sort_saving_by_targetDate() -> pd.DataFrame:
    savingDF = read_savings()
    savingDF = savingDF.sort_values('date')
    return savingDF

# print(getTargetAmount(1))
# print(getCurrentAmount(1))
# print(getStartDate(1))
# updateCurrentAmount(1, 300000)
# print(getTargetAmount(1))
# print(getCurrentAmount(1))