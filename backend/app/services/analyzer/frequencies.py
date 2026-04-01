import pandas as pd
from io import BytesIO
<<<<<<< HEAD
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
=======
from app.services.recoder.schema import Question

def calculate_frequencies_table(mapping:list[Question]):
    df = pd.read_csv("/Users/mateusz/Desktop/Projekty/Tally/backend/app/server/data.csv")
    buffer = BytesIO()
    for col in mapping:
        if col.cafeteria is None:
            question = df[col.question]

            continue
        cafeteria_vals = [c.value for c in col.cafeteria]
        categorical_question = pd.Categorical(df[col.question], cafeteria_vals)
        
>>>>>>> b6ead16 (Working on frontend parsing)
