import pandas as pd

def calculate_frequencie_table():
    df = pd.read_csv("/Users/mateusz/Desktop/Projekty/Tally/Tally/backend/app/server/data.csv")

    print(df)

calculate_frequencie_table()