from .parser import Parser
from bs4 import UnicodeDammit
from io import BytesIO
import pandas as pd

class Recoder:
    def __init__(self, file, filename):
        self.file = file
        self.filename = filename
        self.df: pd.DataFrame | None = None
        self.encoding = self._detect_encoding_with_unicode_dammit(self.file)
        self.df = self._excel_to_dataframe(self.file, self.filename, self.encoding) 
        print(self.df)
        self.parser = Parser(self.df)

    def _detect_encoding_with_unicode_dammit(self, excel:BytesIO) -> str | None:
        """
        Wykrywa encoding używając UnicodeDammit
    
        Args:
            excel: zawartośc pliku jako strumień bajtów

        Returns:
            str | None
        """
        try:
            content =  excel.read()
            suggestion = UnicodeDammit(content)
            return suggestion.original_encoding
        except Exception as e:
            raise ValueError("An error occurred with UnicodeDammit") from e

    def _excel_to_dataframe(self, excel:BytesIO, filename:str, encoding:str | None) -> pd.DataFrame:
        """
        Czyta .csv lub .xlsx do obiektu pandas DataFrame

        Args:
            excel: zawartośc pliku jako strumień bajtów
            filename: oryginalna nazwa pliku
            encoding: encoding pliku jeżeli istnieje

        Returns:
            pd.DataFrame

        Raises:
            ValueError: przesłany plik nie jest plikiem excela
            ValueError: Brak nazwy pliku
        """
        if not filename:
            raise ValueError("Brak nazwy pliku")
        excel.seek(0)
        if filename.endswith(".csv"):
            return pd.read_csv(excel, encoding=encoding)
        elif filename.endswith(".xlsx"):
            return pd.read_excel(excel)
        else:
            raise ValueError("Przesłany plik nie jest plikiem Excela.")


    