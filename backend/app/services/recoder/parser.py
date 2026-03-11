import pandas as pd

from .iterator import QuestionIterator
from bs4 import UnicodeDammit
from io import BytesIO

def main(excel:BytesIO, filename:str):
    """
    Parsuje plik ankiety do listy pytań z kafeterią.

    Wykrywa encoding, wczytuje plik do DataFrame,
    a następnie iteruje po kolumnach budując obiekty Question.

    Args:
        excel: zawartość pliku jako strumień bajtów
        filename: oryginalna nazwa pliku (używana do wykrycia formatu)

    Returns:
        list[Question]
    """
    encoding = detect_encoding_with_unicode_dammit(excel)
    df:pd.DataFrame = excel_to_dataframe(excel=excel, 
                                         filename=filename, 
                                         encoding=encoding)
    iterator = QuestionIterator(df)
    pass

def detect_encoding_with_unicode_dammit(excel:BytesIO) -> str | None:
    """
    Wykrywa encoding używając UnicodeDammit z Beautiful Soup
    
    Args:
        excel: zawartośc pliku jako strumień bajtów

    Returns:
        str | None
    """
    try:
        content = excel.read()
        suggestion = UnicodeDammit(content)
        return suggestion.original_encoding
    except Exception as e:
        raise ValueError("An error occurred with UnicodeDammit") from e

def excel_to_dataframe(excel:BytesIO, filename:str, encoding:str | None) -> pd.DataFrame:
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