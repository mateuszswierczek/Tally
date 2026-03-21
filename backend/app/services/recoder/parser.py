import pandas as pd
import json

from .iterator import QuestionIterator

class Parser:
    """
    Parsuje plik ankiety do listy pytań z kafeterią.
    """
    def __init__(self, df:pd.DataFrame):
        self.iterator = QuestionIterator(df)
        self._grouped_data = []
        self.mapping_data = []

    def iterate(self):
        for question in self.iterator.iterate():
            self._grouped_data.append(question)
            
    def _create_mapping(self):
        for question in self._grouped_data:
            question["cafeteria"] = [json.dumps(c) for c in question["cafeteria"]]