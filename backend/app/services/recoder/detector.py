import re

from typing import Literal
from .schema import ColumnType 

class Detector:
    MISSING_VALUES = ["", "#N/A", "N/A"]
    MISSING_VALUES_CODES = {"SysMissing":MISSING_VALUES}
    NUMERICAL:list[str] = ["int64", "float64"]
    SUBQUESTION_PATTERN = re.compile(r'^(.+?)\s*\[.+\]$')
    THRESHOLD_5:int = 5
    THRESHOLD_10:int = 10

    def detect_column_type(self, unique_values:int, column_dtype) -> Literal["nominal", "ordinal", "continuous", "text"]:
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
        if unique in self.MISSING_VALUES:
            return True
        return False 

    def assign_missing_code(self, unique:str, is_missing:bool) -> str | None:
        if not is_missing:
            return None
        for key, val in self.MISSING_VALUES_CODES.items():
            if unique in val:
                return key
        return None

    def get_base_question(self, col: str) -> str | None:
        if match := self.SUBQUESTION_PATTERN.match(col):
            return match.group(1).strip()
        return None