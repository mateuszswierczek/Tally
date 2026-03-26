import pandas as pd
from .schema import Question

def map_coding_onto_database(mapping:list[Question], df:pd.DataFrame):
    for question in mapping:
        if question.cafeteria_dump is None:
            continue
        df[question.question] = df[question.question].map({c["value"]: c["index"] for c in question.cafeteria_dump})
    return df