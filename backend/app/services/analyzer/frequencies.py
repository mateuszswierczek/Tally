import pandas as pd
from io import BytesIO
from app.services.recoder.serializer import Serializer

def calculate_frequencie_table():
    df = pd.read_csv("/Users/mateusz/Desktop/Projekty/Tally/Tally/backend/app/server/data.csv")
    buffer = BytesIO()
    serializer = Serializer()
    mapping_data = serializer.deserialize()
    for col in mapping_data:
        if col.cafeteria is not None:
            cafetaria_vars = [c.value for c in col.cafeteria]
            print(cafetaria_vars)
            question_categorical = pd.Categorical(df[col.question], cafetaria_vars)
            #print(question_categorical)

calculate_frequencie_table()