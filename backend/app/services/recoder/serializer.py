import pandas as pd
import json
import os

from .schema import Question

class Serializer:
    """Zapis i odczyt listy Question do/z pliku JSON."""

    def serialize(self, question:list[Question]):
        """Zapisuje listę Question do questions.json."""
        model = [c.model_dump() for c in question]
        with open("questions.json", 'w') as f:
            json.dump(model, f)

    def deserialize(self) -> list[Question]:
        """Wczytuje questions.json i zwraca listę Question."""
        question_data = None
        if not os.path.exists("questions.json"):
            pass
        
        with open("questions.json", 'r') as f:
                question_data = json.loads(f.read())

        question = []

        for q in question_data:
            question.append(Question(
                question=q["question"],
                index=q["index"],
                type=q["type"],
                unique_count=q["unique_count"],
                missing_count=q["missing_count"],
                total_count=q["total_count"],
                cafeteria=q["cafeteria"]
            ))
        if question == None:
             raise ValueError()
        return question
