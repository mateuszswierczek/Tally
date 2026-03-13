from app.services.recoder.iterator import QuestionIterator
from app.services.recoder.schema import Question

import pandas as pd
import unittest

class TestQuestionIterator(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "Q1": ["Tak", "Nie", "Nie wiem", None, "Tak", "Tak", "Nie"],
            "Q2 [SQ001]": ["A", "B", "A", "C", "C", "C", "A"],
            "Q2 [SQ002]": ["X", "Y", "X", "Y", "A", "A", "B"],
        })
        self.iterator = QuestionIterator(self.df)

    def test_create_iteration_object(self):
        assert self.iterator._grouped == {"Q2" : ["Q2 [SQ001]", "Q2 [SQ002]"]}

    def test_iterate_object_type(self):
        assert isinstance(next(self.iterator.iterate()), Question)

    def test_iterate_unique_size(self):
        assert next(self.iterator.iterate()).unique_count == 3

    def test_iterate_question(self):
        assert next(self.iterator.iterate()).question == "Q1"
    
    def test_iterate_index(self):
        assert next(self.iterator.iterate()).index == 1
    
    def test_iterate_type(self):
        assert next(self.iterator.iterate()).type == "nominal"

    def test_iterate_missing_count(self):
        assert next(self.iterator.iterate()).missing_count == 1
    
    def test_iterate_total_count(self):
        assert next(self.iterator.iterate()).total_count == 6
    