import pandas as pd

from .schema import Question, Cafeteria
from .detector import Detector
from typing import Generator

class QuestionIterator:
    """Iteruje kolumny DataFrame, grupuje podpytania i buduje obiekty Question z kafeterią."""

    COLS_TO_DROP = ["ID odpowiedzi", "Data zakończenia", "Ostatnia strona", "Język początkowy", "pid", "Inne"]

    def __init__(self, df:pd.DataFrame) -> None:
        self.df:pd.DataFrame = df
        self.detector = Detector()
        self._grouped:dict[str, list[str]] = self._create_iteration_object()

    def _create_iteration_object(self) -> dict:
        """Buduje mapę pytanie_główne → [kolumny podpytań]."""
        grouped:dict[str, list[str]]= {}
        for col in self.df.columns:
            if match := self.detector.get_base_question(col):
                grouped.setdefault(match, []).append(col)
        return grouped

    def iterate(self) -> Generator[Question]:
        """Yield Question dla każdej kolumny; łączy podpytania w jedno pytanie matrycowe."""
        temp_subquestions: list[Question] = []
        index_number = 1
        
        for _, col in enumerate(self.df.columns, start=1):
            unique_size: int = self.df[col].dropna().unique().shape[0]
            total_count: int = self.df[col].dropna().shape[0]
            column_type = self.detector.detect_column_type(unique_size, self.df[col].dtype)
            is_grouped = any(col in cols for cols in self._grouped.values())

            if any(col_to_drop in col for col_to_drop in self.COLS_TO_DROP):
                continue

            if is_grouped:
                if temp_subquestions:
                    first_q = temp_subquestions[0]
                    if self.detector.get_base_question(col) != self.detector.get_base_question(str(first_q.question)):
                        yield self._iterate_subquestion(temp_subquestions)
                        temp_subquestions = []
                        index_number += 1
                temp_subquestions.append(self._make_question(col, index_number, column_type, unique_size, total_count))
                
            else:
                if temp_subquestions:
                    yield self._iterate_subquestion(temp_subquestions)
                    temp_subquestions = []
                    index_number += 1
                
                yield self._make_question(col, index_number, column_type, unique_size, total_count)
                index_number += 1

        if temp_subquestions:
            yield self._iterate_subquestion(temp_subquestions)

    def _make_question(self, col, index_number, column_type, unique_size, total_count) -> Question:
        """Tworzy obiekt Question dla pojedynczej kolumny."""
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
        return question

    def _iterate_cafeteria(self, column:pd.Series, total_count:int) -> list:
        """Buduje kafeterię (listę Cafeteria) z unikalnych wartości kolumny."""
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

    def _iterate_subquestion(self, temp_subquestions) -> Question:
        """Scala listę podpytań w jedno pytanie główne ze wspólną kafeterią."""
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
            subquestions = [q for q in temp_subquestions],
        )
        return question

    def _iterate_subquestions_cafeteria(self, subquestion:list[Question]) -> dict:
        """Zbiera unikalne wartości kafeterii ze wszystkich podpytań i mapuje je na indeksy."""
        cafe_values = []
        for q in subquestion:
            cafe = q.cafeteria
            if cafe:
                for c in cafe:
                    cafe_values.append(c.value)
        
        unique_cafe_values = set(cafe_values)
        subquestion_cafeteria_mapping = {ind:val for ind, val in enumerate(list(unique_cafe_values))}
        return subquestion_cafeteria_mapping
        