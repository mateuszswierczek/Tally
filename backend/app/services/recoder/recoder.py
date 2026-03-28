from .parser import Parser
from bs4 import UnicodeDammit
from io import BytesIO
import pandas as pd

class Recoder:

    def __init__(self, file, filename):
        self.file = file
        self.filename = filename
        self.encoding = self._detect_encoding_with_unicode_dammit(self.file)
        self.df:pd.DataFrame = self._excel_to_dataframe(self.file, self.filename, self.encoding)
        self.parser = Parser(self.df)

    def _detect_encoding_with_unicode_dammit(self, excel:BytesIO) -> str | None:
        try:
            content =  excel.read()
            suggestion = UnicodeDammit(content)
            return suggestion.original_encoding
        except Exception as e:
            raise ValueError("An error occurred with UnicodeDammit") from e
    
    def save_db(self):
        self.df.to_csv('/Users/mateusz/Desktop/Projekty/Tally/Tally/backend/app/server/data.csv', encoding='utf-8')

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