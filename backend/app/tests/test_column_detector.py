from fixtures.columns import ORDINAL_COLUMN, CONTINUOUS_COLUMN, NOMINAL_COLUMN
from app.services.recoder.detector import detect_column_type, is_missing_unique, assign_missing_code, get_base_question

import unittest

class TestDetectorMethods(unittest.TestCase):

    def test_detect_column_ordinal(self):
        assert detect_column_type(len(ORDINAL_COLUMN["values"]), object) == "ordinal"

    def test_detect_column_continuous(self):
        assert detect_column_type(len(CONTINUOUS_COLUMN["values"]), "int64") == "continuous"

    def test_detect_column_nominal(self):
        assert detect_column_type(len(NOMINAL_COLUMN["values"]), object) == "nominal"

    def test_is_missing(self):
        assert is_missing_unique("N/A") == True

    def test_assign_missing_code(self):
        assert assign_missing_code("#N/A", True) == "SysMissing"

    def test_get_base_question(self):
        assert get_base_question("Oceń od 1 do 10 ['Czekolada']") == "Oceń od 1 do 10"