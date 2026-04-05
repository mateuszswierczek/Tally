import pandas as pd

from app.services.recoder.schema import Question
from typing import Generator

def generate_frequencies_table(mapping:list[Question]) -> Generator[pd.DataFrame]:
    df = pd.read_csv("/Users/mateusz/Desktop/Projekty/Tally/backend/app/server/data.csv")
    for col in mapping:
        if col.cafeteria is None:
            question = df[col.question]
            value_counts = question.value_counts().reset_index(name="Częstości")
            value_counts["% z N"] = value_counts["Częstości"] / col.total_count
            yield value_counts
        elif col.subquestions is not None:
            main_mapping = col.cafeteria
            pass
            # for subq in col.subquestions:
            #     pass
        else:
            cafeteria_vals = [c.value for c in col.cafeteria]
            categorical_question = pd.Categorical(df[col.question], cafeteria_vals)
            value_counts = categorical_question.value_counts().reset_index(name="Częstości")
            value_counts["% z N"] = value_counts["Częstości"] / col.total_count
            yield value_counts