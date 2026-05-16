import pandas as pd
from .schema import Question
from .serializer import Serializer

class Mapper:
    def __init__(self, df:pd.DataFrame):
        self.df = df.copy()
        self.serializer = Serializer()

    def map_coding_onto_database(self, mapping:list[Question], df:pd.DataFrame) -> pd.DataFrame:
        df_copy = df.copy()

        for question in mapping:
            if question.cafeteria_dump is None:
                continue
            if question.subquestions is not None:
                main_mapping = {c["value"]: c["index"] for c in question.cafeteria_dump}
                for subquestion in question.subquestions:
                    df_copy[subquestion.question] = df_copy[subquestion.question].map(main_mapping)
                continue
            df_copy[question.question] = df_copy[question.question].map({c["value"]: c["index"] for c in question.cafeteria_dump})
        return df_copy
    
    def create_book_of_codes(self, mapping:list[Question]) -> pd.DataFrame:
        df_of_codes = pd.DataFrame()
        for question in mapping:
            if question.cafeteria_dump is None:
                continue
            temp_df = pd.DataFrame({"Nazwa pytania":question.question, "":[""]})
            df_of_codes = pd.concat([df_of_codes, temp_df])
            temp_df = pd.DataFrame({"Nazwa pytania":[value["value"] for value in question.cafeteria_dump], "":[value["index"] for value in question.cafeteria_dump]})
            df_of_codes = pd.concat([df_of_codes, temp_df])
            temp_df = pd.DataFrame({"Nazwa pytania":[""], "":[""]})
            df_of_codes = pd.concat([df_of_codes, temp_df])

        return df_of_codes
  