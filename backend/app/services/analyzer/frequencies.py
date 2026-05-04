import pandas as pd
from app.services.recoder.schema import Question
from app.services.recoder.detector import Detector
from typing import Generator

def generate_frequencies_table(mapping:list[Question]) -> Generator[tuple[pd.DataFrame, pd.Series | pd.DataFrame | None]]:
    df = pd.read_csv("/Users/mateusz/Desktop/Projekty/Tally/backend/app/server/data.csv")
    for col in mapping:
        if col.cafeteria is None:
            # other_question = _create_value_counts_table(df[col.question], col) 
            # _add_columnt_tile(other_question, col)
            try:
                other_question = _create_value_counts_table(
                    pd.Categorical(df[col.question], 
                    [unique for unique in df[col.question].unique()].sort(), ordered=True),col)
                _add_columnt_tile(other_question, col)
            except:
                other_question = _create_value_counts_table(df[col.question], col) 
                _add_columnt_tile(other_question, col)
            
            yield other_question, other_question.drop(columns="Częstości")
        elif col.subquestions is not None:
            if col.is_maq:
                complex_table = _create_maq_table(col.subquestions, df, col)
                assert complex_table is not None
                _add_columnt_tile(complex_table, col)
                yield complex_table, complex_table.drop(columns="Częstości")
            else:
                matrix_table = _create_matrix_percentage(col.subquestions, df, col)
                _add_columnt_tile(matrix_table, col)
                for ind, inner_col in enumerate(col.subquestions):
                    categorical_question = _create_value_counts_table(
                        pd.Categorical(df[inner_col.question], 
                        [cafe.value for cafe in col.cafeteria]),col)
                    _add_columnt_tile(categorical_question, inner_col)
                    yield categorical_question, matrix_table if ind == 0 else None
        else:
            categorical_question = _create_value_counts_table(
                pd.Categorical(df[col.question], 
                [cafe.value for cafe in col.cafeteria]),col)
            _add_columnt_tile(categorical_question, col)
            yield categorical_question, categorical_question.drop(columns="Częstości")

def _create_value_counts_table(question:pd.Series | pd.Categorical | pd.DataFrame, col:Question):
    value_counts = question.value_counts().reset_index(name="Częstości")
    value_counts["% z N"] = (value_counts["Częstości"] / col.total_count) * 100
    return value_counts

def _add_columnt_tile(question:pd.DataFrame, col:Question):
    try:
        question.rename(columns={"index": " "})
        question.insert(0, col.question, " ")
    except:
        try:
            question.insert(0, col.question, " ")
        except:
            return

def _create_maq_table(subquestions:list[Question], df:pd.DataFrame, col:Question):
    detector = Detector()
    assert col.cafeteria_dump
    main_mapping = {cafe["value"]:cafe["index"] for cafe in col.cafeteria_dump}
    subquestions_columns = [subq.question for subq in subquestions]
    matrix_df = df[subquestions_columns]
    matrix_df.columns = [detector.get_cafeteria_item(matrix_col) for matrix_col in matrix_df.columns]
    for column in matrix_df.columns:
        matrix_df[column] = matrix_df[column].map(main_mapping)
    matrix_df = matrix_df.sum().reset_index(name="Częstości")
    matrix_df["% z N"] = matrix_df["Częstości"] / col.total_count
    matrix_df["% z Odpowiedzi"] = (matrix_df["Częstości"] / matrix_df["Częstości"].sum()).round(2)
    return matrix_df

def _create_matrix_percentage(subquestions:list[Question], df:pd.DataFrame, col:Question):
    detector = Detector()
    subquestions_columns = [subq.question for subq in subquestions]
    matrix_df:pd.DataFrame = df[subquestions_columns]
    matrix_df.columns = [detector.get_cafeteria_item(matrix_col) for matrix_col in matrix_df.columns]
    result = _create_value_counts_table(matrix_df.melt(), col)
    pivoted = result.pivot(columns="value", index="variable").fillna(0)
    pivoted.columns = pivoted.columns.droplevel(0)
    pivoted = pivoted.iloc[:, col.unique_count:].reset_index()
    return pivoted