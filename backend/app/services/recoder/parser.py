import pandas as pd

from .iterator import QuestionIterator

class Parser:
    def __init__(self, df:pd.DataFrame):
        self.iterator = QuestionIterator(df)
        self._grouped_data = []
        self.mapping_data = []

    def iterate(self):
        for question in self.iterator.iterate():
            self._grouped_data.append(question)
        self._create_mapping()

    def _create_mapping(self):
        self.mapping_data = self._grouped_data
        for question in self.mapping_data:
            if question.cafeteria == None:
                continue
            question.cafeteria_dump = [dict(c) for c in question.cafeteria]
            