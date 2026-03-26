from .parser import Parser
from bs4 import UnicodeDammit
from io import BytesIO
from .mapper import map_coding_onto_database
import pandas as pd

class Recoder:
    _df: pd.DataFrame | None = None

    def __init__(self, file, filename):
        self.file = file
        self.filename = filename
        self.encoding = self._detect_encoding_with_unicode_dammit(self.file)
        self.df = self._excel_to_dataframe(self.file, self.filename, self.encoding)
        Recoder._df = self.df
        self.parser = Parser(self.df)

    @classmethod
    def get_df(cls) -> pd.DataFrame:
        if cls._df is None:
            raise RuntimeError("")
        return cls._df

    def _detect_encoding_with_unicode_dammit(self, excel:BytesIO) -> str | None:
        try:
            content =  excel.read()
            suggestion = UnicodeDammit(content)
            return suggestion.original_encoding
        except Exception as e:
            raise ValueError("An error occurred with UnicodeDammit") from e

    @staticmethod
    def _excel_to_dataframe(excel:BytesIO, filename:str, encoding:str | None) -> pd.DataFrame:
        if not filename:
            raise ValueError("Brak nazwy pliku")
        excel.seek(0)
        if filename.endswith(".csv"):
            return pd.read_csv(excel, encoding=encoding)
        elif filename.endswith(".xlsx"):
            return pd.read_excel(excel)
        else:
            raise ValueError("Przesłany plik nie jest plikiem Excela.")

    @staticmethod
    def map_coding(mapping, df):
        df_mapped = map_coding_onto_database(mapping, df)
        return df_mapped