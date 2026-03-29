import pandas as pd
from .schema import Question

class Mapper:
    def __init__(self, data_path:str):
        self.df = self.load(data_path)

    def load(self, data_path):
        try:
            return pd.read_csv(data_path)
        except Exception:
            raise ValueError()

    def map_coding_onto_database(self, mapping:list[Question], df:pd.DataFrame):
        df_copy = df.copy()
        for question in mapping:
            if question.cafeteria_dump is None:
                continue
            df_copy[question.question] = df_copy[question.question].map({c["value"]: c["index"] for c in question.cafeteria_dump})
        return df_copy