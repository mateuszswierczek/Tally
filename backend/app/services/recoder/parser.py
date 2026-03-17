import pandas as pd

from .iterator import QuestionIterator

class Parser:
    """
    Parsuje plik ankiety do listy pytań z kafeterią.
    """
    def __init__(self, df:pd.DataFrame):
        self.iterator = QuestionIterator(df)
        self._grouped_data = []

    def iterate(self):
        for question in self.iterator.iterate():
            self._grouped_data.append(question)
            print(question)