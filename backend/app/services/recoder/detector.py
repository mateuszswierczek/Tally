import re

from typing import Literal
from .schema import ColumnType 

class Detector:
    """Klasyfikuje kolumny DataFrame — typy zmiennych, brakujące wartości, podpytania."""

    MISSING_VALUES = ["", "#N/A", "N/A"]
    MISSING_VALUES_CODES = {"SysMissing":MISSING_VALUES}
    NUMERICAL:list[str] = ["int64", "float64"]
    SUBQUESTION_PATTERN = re.compile(r'^(.+?)\s*\[.+\]$')
    THRESHOLD_5:int = 5
    THRESHOLD_10:int = 10

    def detect_column_type(self, unique_values:int, column_dtype) -> Literal["nominal", "ordinal", "continuous", "text"]:
        """Przypisuje typ statystyczny kolumny na podstawie liczby unikalnych wartości i dtype."""
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
        """Sprawdza czy wartość jest brakiem danych."""
        if unique in self.MISSING_VALUES:
            return True
        return False

    def assign_missing_code(self, unique:str, is_missing:bool) -> str | None:
        """Zwraca kod braku (np. 'SysMissing') lub None."""
        if not is_missing:
            return None
        for key, val in self.MISSING_VALUES_CODES.items():
            if unique in val:
                return key
        return None

    def get_base_question(self, col: str) -> str | None:
        """Zwraca nazwę pytania głównego z kolumny w formacie 'Pytanie [podpytanie]'."""
        if match := self.SUBQUESTION_PATTERN.match(col):
            return match.group(1).strip()
        return None

    def get_cafeteria_item(self, col: str) -> str | None:
        """Zwraca zawartość nawiasów kwadratowych z nazwy kolumny."""
        return "".join(re.findall(r'\[([^\]]*)\]', col))