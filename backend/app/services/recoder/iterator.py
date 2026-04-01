import pandas as pd

from .schema import Question, Cafeteria
from .detector import Detector

class QuestionIterator:
    def __init__(self, df:pd.DataFrame) -> None:
        self.df:pd.DataFrame = df
        self.detector = Detector()
        self._grouped:dict[str, list[str]] = self._create_iteration_object()

    def _create_iteration_object(self):
        grouped:dict[str, list[str]]= {}
        for col in self.df.columns:
            if match := self.detector.get_base_question(col):
                grouped.setdefault(match, []).append(col)
        return grouped

    def iterate(self):
<<<<<<< HEAD
        #TODO: Obsługa 'Subquestion'
=======
        temp_subquestions:list[Question] = []
        index_number = 1
>>>>>>> b6ead16 (Working on frontend parsing)
        for ind, col in enumerate(self.df.columns, start=1):
            unique_size:int = self.df[col].dropna().unique().shape[0]
            total_count:int = self.df[col].dropna().shape[0]
            column_type = self.detector.detect_column_type(unique_size, self.df[col].dtype)

<<<<<<< HEAD
            question = Question(
                question=col,
                index=ind,
=======
            if temp_subquestions:
                first_question = temp_subquestions[0]
                if (first_question and self.detector.get_base_question(col) != self.detector.get_base_question(str(first_question.question))) or (first_question and ind == len(self.df.columns)):
                    question = Question(
                        question=self.detector.get_base_question(str(first_question.question)),
                        index=first_question.index,
                        type=first_question.type,
                        unique_count=first_question.unique_count,
                        missing_count=first_question.missing_count,
                        total_count=first_question.total_count,
                        cafeteria=first_question.cafeteria,
                        subquestions = [q for q in temp_subquestions]
                    )
                    temp_subquestions = []
                    index_number += 1
                    yield question

            question = Question(
                question=col,
                index=index_number,
>>>>>>> b6ead16 (Working on frontend parsing)
                type=column_type,
                unique_count=unique_size,
                missing_count=self.df[col].isna().sum(),
                total_count=total_count,
<<<<<<< HEAD
                cafeteria=(self._iterate_cafeteria(self.df[col].dropna(), total_count)
                    if column_type == "nominal" or 
                    column_type ==  "ordinal" else None)

            )
=======
                cafeteria=(self._iterate_cafeteria(self.df[col].dropna(), total_count) 
                           if column_type == "nominal" or 
                           column_type ==  "ordinal" else None),
                subquestions = None
                )
            
            if any(col in cols for cols in self._grouped.values()):
                temp_subquestions.append(question)
                continue

            print(col)
            index_number += 1
>>>>>>> b6ead16 (Working on frontend parsing)
            yield question

    def _iterate_cafeteria(self, column:pd.Series, total_count:int):
        temp = []
        counts = column.value_counts().T
        for ind, unique in enumerate(column.unique(), start=1):
            is_missing = self.detector.is_missing_unique(unique)
            cafeteria = Cafeteria(
                value = unique,
                index = ind,
                n = counts[unique],
                pct = counts[unique]/total_count,
                is_missing=is_missing,
                missing_code=self.detector.assign_missing_code(unique, is_missing)
            )
            temp.append(cafeteria)
        return temp
