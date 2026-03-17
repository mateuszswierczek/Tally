import re

from typing import Literal
from .schema import ColumnType 

class Detector:
#=========================================================
#CONSTANTS
#=========================================================
    MISSING_VALUES = ["", "#N/A", "N/A"]
    MISSING_VALUES_CODES = {"SysMissing":MISSING_VALUES}
    NUMERICAL:list[str] = ["int64", "float64"]
    SUBQUESTION_PATTERN = re.compile(r'^(.+?)\s*\[.+\]$')
    THRESHOLD_5:int = 5
    THRESHOLD_10:int = 10

    def detect_column_type(self, unique_values:int, column_dtype) -> Literal["nominal", "ordinal", "continuous", "text"]:
        """
        Określa typ pytania na podstawie liczby unikatowy itemów w kafeterii
        i typu danych z obiektu pd.Series

        Args:
            unique_values: Liczba unikatowych itemów w kafeterii
            column_dtype: Typ danych columny

        Returns:
            Poziom zmiennej jako string z listy ["nominal", "ordinal", "continuous", "text"]
        """

        if unique_values < self.THRESHOLD_5 and column_dtype == object:
            return ColumnType.nominal.value
        if ((unique_values >= self.THRESHOLD_5 and unique_values <= self.THRESHOLD_10) and
            column_dtype == object):
            return ColumnType.ordinal.value
        if column_dtype in self.NUMERICAL:
            return ColumnType.continuous.value
        if ((unique_values > self.THRESHOLD_10) and
            column_dtype == object):
            return ColumnType.text.value
        else:
            return ColumnType.nominal.value
    
    def is_missing_unique(self, unique:str) -> bool:
        """
        Sprawdza, czy wartość itemu z kafeterii jest brakiem danych.

        Args:
            unique: item z kafeterii

        Returns:
            True, jeżeli tak, w innym wypadku False
        """
        if unique in self.MISSING_VALUES:
            return True
        return False 

    def assign_missing_code(self, unique:str, is_missing:bool) -> str | None:
        """
        Przypisuje kod braku danych, jeżeli item z kafeterii jest brakiem danych.

        Args:
            unique: item z kafeterii
            is_missing: czy item jest brakiem danych

        Returns:
            Kod braku pytania jeżeli is_missing, w innym wypadku None
        """
        if not is_missing:
            return None
        for key, val in self.MISSING_VALUES_CODES.items():
            if unique in val:
                return key
        return None

    def get_base_question(self, col: str) -> str | None:
        """
            Sprawdza, czy w treści pytania znajduje się '[...]' (Pytania matrycowe lub wielokrotnego wyboru)

            Args:
                col: treść pytania

            Returns:
                Treść pytania bez '[...]' jeżeli '[...]' znajduje się w treści pytania, w innym wypadku None
        """
        if match := self.SUBQUESTION_PATTERN.match(col):
            return match.group(1).strip()
        return None