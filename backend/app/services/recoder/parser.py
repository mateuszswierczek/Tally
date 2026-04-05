import pandas as pd

from .iterator import QuestionIterator
from .serializer import Serializer

class Parser:
    """
    Parsuje plik ankiety do listy pytań z kafeterią.
    """
    def __init__(self, df:pd.DataFrame):
        self.iterator = QuestionIterator(df)
        self.serializer = Serializer()
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

    def save_model_to_json(self):
        self.serializer.serialize(self.mapping_data)
            