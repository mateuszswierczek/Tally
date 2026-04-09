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
            print(col.is_maq)
            if col.is_maq:
                complex_table = _create_maq_table(col.subquestions, df, col)
            else:
                complex_table = _create_matrix_table(col.subquestions, df, col)
            yield complex_table #type:ignore
        else:
            yield _create_value_counts_table(
                pd.Categorical(df[col.question], 
                [cafe.value for cafe in col.cafeteria]),col)

def _create_value_counts_table(question:pd.Series | pd.Categorical | pd.DataFrame, col:Question):
    value_counts = question.value_counts().reset_index(name="Częstości")
    value_counts["% z N"] = value_counts["Częstości"] / col.total_count
    return value_counts

#Refaktoryzacja + % w kolumnach
def _create_maq_table(subquestions:list[Question], df:pd.DataFrame, col:Question):
    detector = Detector()
    temp_cafe = {cafe["index"]:cafe["value"] for cafe in col.cafeteria_dump} #type: ignore
    main_cafeteria_mapping_sorted = dict(sorted(temp_cafe.items()))
    subquestions_columns = [subq.question for subq in subquestions]
    matrix_df = df[subquestions_columns]
    matrix_df.columns = [detector.get_cafeteria_item(matrix_col) for matrix_col in matrix_df.columns]
    print(matrix_df)

#TODO: Refaktoryzacja + % w kolumnach
def _create_matrix_table(subquestions:list[Question], df:pd.DataFrame, col:Question):
    detector = Detector()
    temp_cafe = {cafe["index"]:cafe["value"] for cafe in col.cafeteria_dump} #type: ignore
    main_cafeteria_mapping_sorted = dict(sorted(temp_cafe.items()))
    subquestions_columns = [subq.question for subq in subquestions]
    matrix_df = df[subquestions_columns]
    matrix_df.columns = [detector.get_cafeteria_item(matrix_col) for matrix_col in matrix_df.columns]
    value_counts = _create_value_counts_table(matrix_df.melt(), col)
    pivoted = value_counts.pivot(columns="value", index="variable").fillna(0)
    pivoted.columns = pivoted.columns.droplevel(0)
    pivoted = pivoted[list(main_cafeteria_mapping_sorted.values())]
    return pivoted