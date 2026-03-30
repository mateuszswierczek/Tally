import pandas as pd
import json

from .schema import Question

class Serializer:
    def serialize(self, question:list[Question]):
        question_dump = [q.model_dump_json() for q in question]
        with open("questions.json", 'w') as f:
            json.dump(question_dump, f)

    def deserialize(self):
        pass