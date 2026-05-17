from fixtures.columns import ORDINAL_COLUMN, CONTINUOUS_COLUMN, NOMINAL_COLUMN
from app.services.recoder.detector import Detector

import unittest

class TestDetectorMethods(unittest.TestCase):
    def __init__(self):
        self.detector = Detector()
    def test_detect_column_ordinal(self):
        assert self.detector.detect_column_type(len(ORDINAL_COLUMN["values"]), object) == "ordinal"

    def test_detect_column_continuous(self):
        assert self.detector.detect_column_type(len(CONTINUOUS_COLUMN["values"]), "int64") == "continuous"

    def test_detect_column_nominal(self):
        assert self.detector.detect_column_type(len(NOMINAL_COLUMN["values"]), object) == "nominal"

    def test_is_missing(self):
        assert self.detector.is_missing_unique("N/A") == True

    def test_assign_missing_code(self):
        assert self.detector.assign_missing_code("#N/A", True) == "SysMissing"

    def test_get_base_question(self):
        assert self.detector.get_base_question("Oceń od 1 do 10 ['Czekolada']") == "Oceń od 1 do 10"