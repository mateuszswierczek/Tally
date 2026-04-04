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
        temp_subquestions:list[Question] = []
        index_number = 1
        for ind, col in enumerate(self.df.columns, start=1):
            unique_size:int = self.df[col].dropna().unique().shape[0]
            total_count:int = self.df[col].dropna().shape[0]
            column_type = self.detector.detect_column_type(unique_size, self.df[col].dtype)

            if temp_subquestions:
                first_question = temp_subquestions[0]
                if ((first_question and
                    self.detector.get_base_question(col) != self.detector.get_base_question(str(first_question.question)))
                    or (first_question and ind == len(self.df.columns))):
                   
                    yield self._iterate_subquestion(temp_subquestions)
                    temp_subquestions = []
                    index_number += 1

            question = Question(
                question=col,
                index=index_number,
                type=column_type,
                unique_count=unique_size,
                missing_count=self.df[col].isna().sum(),
                total_count=total_count,
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

    #TODO: Refaktoryzacja 
    def _iterate_subquestion(self, temp_subquestions) -> Question:
        first_question = temp_subquestions[0]
        cafeteria_dict = pd.Series(self._iterate_subquestions_cafeteria(temp_subquestions))
        main_question_cafeteria = self._iterate_cafeteria(cafeteria_dict, first_question.total_count)
        question = Question(
            question=self.detector.get_base_question(str(first_question.question)),
            index=first_question.index,
            type=first_question.type,
            unique_count=first_question.unique_count,
            missing_count=first_question.missing_count,
            total_count=first_question.total_count,
            cafeteria=main_question_cafeteria,
            subquestions = [q for q in temp_subquestions]
        )
        return question

    #TODO:  Nazwy zmiennych, refaktoryzacja
    def _iterate_subquestions_cafeteria(self, subquestion:list[Question]):
        temp_cafe = []
        for q in subquestion:
            cafe = q.cafeteria
            if cafe:
                for c in cafe:
                    temp_cafe.append(c.value)
        
        temp_subquestions_set = set(temp_cafe)
        temp_subquestions_list = list(temp_subquestions_set)
        subquestion_cafeteria_mapping = {ind:val for ind, val in enumerate(temp_subquestions_list)}
        return subquestion_cafeteria_mapping
        