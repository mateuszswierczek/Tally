import pandas as pd

from app.services.recoder.schema import Question
from app.services.recoder.detector import Detector
from typing import Generator

def generate_frequencies_table(mapping:list[Question]) -> Generator[pd.DataFrame]:
    df = pd.read_csv("/Users/mateusz/Desktop/Projekty/Tally/backend/app/server/data.csv")
    for col in mapping:
        if col.cafeteria is None:
            yield _create_value_counts_table(df[col.question], col)
        elif col.subquestions is not None:
            if col.is_maq:
                pass
            #TODO: Sprawdzić czy jak policzę kazdy subquestions osobno 
            # i potem scale wyniki w jedna tabele to czy to ma sens.
            matrix_table = _create_matrix_table(col.subquestions, df, col)
            yield matrix_table
        else:
            yield _create_value_counts_table(
                pd.Categorical(df[col.question], 
                [cafe.value for cafe in col.cafeteria]),col)

def _create_value_counts_table(question:pd.Series | pd.Categorical | pd.DataFrame, col:Question):
    value_counts = question.value_counts().reset_index(name="Częstości")
    value_counts["% z N"] = value_counts["Częstości"] / col.total_count
    return value_counts

def _create_matrix_table(subquestions:list[Question], df:pd.DataFrame, col:Question):
    detector = Detector()
    subquestions_columns = [subq.question for subq in subquestions]
    matrix_df = df[subquestions_columns]
    matrix_df.columns = [detector.get_cafeteria_item(matrix_col) for matrix_col in matrix_df.columns]
    matrix_table = _create_value_counts_table(matrix_df.T, col)
    return matrix_table