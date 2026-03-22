import pandas as pd

from .schema import Question, Cafeteria
from .detector import Detector

class QuestionIterator:
    """Iteruje po kolumnach DataFrame budując listę obiektów Question z kafeterią."""

    def __init__(self, df:pd.DataFrame) -> None:
        """
        Args:
            df: DataFrame z danymi ankiety
        """
        self.df:pd.DataFrame = df
        self.detector = Detector()
        self._grouped:dict[str, list[str]] = self._create_iteration_object()

    def _create_iteration_object(self):
        """
        Grupuje kolumny pytań wielokrotnych/macierzowych po tekście bazowym.

        Kolumny w formacie "Pytanie [Podpytanie]" są grupowane po części przed [].
        Kolumny bez [] są pomijane — obsługiwane jako samodzielne pytania w iterate().

        Returns:
            Słownik {tekst_bazowy: [nazwa_kolumny, ...]}
        """
        grouped:dict[str, list[str]]= {}
        for col in self.df.columns:
            if match := self.detector.get_base_question(col):
                grouped.setdefault(match, []).append(col)
        return grouped

    def iterate(self):
        #TODO: Obsługa 'Cafeteria' oraz 'Subquestion'
        """
        Iteruje po kolumnach DataFrame, budując obiekty Question.

        Yields:
            Question: Obiekt Question
        """
        for ind, col in enumerate(self.df.columns, start=1):
            unique_size:int = self.df[col].dropna().unique().shape[0]
            total_count:int = self.df[col].dropna().shape[0]
            column_type = self.detector.detect_column_type(unique_size, self.df[col].dtype)

            question = Question(
                question=col,
                index=ind,
                type=column_type,
                unique_count=unique_size,
                missing_count=self.df[col].isna().sum(),
                total_count=total_count,
                cafeteria=(self._iterate_cafeteria(self.df[col].dropna(), total_count)
                    if column_type == "nominal" or 
                    column_type ==  "ordinal" else None)

            )
            yield question

    def _iterate_cafeteria(self, column:pd.Series, total_count:int):
        """
        Buduje kafeterię dla pojedynczej kolumny.

        Args:
            column: seria bez NaN
            total_count: liczba odpowiedzi bez NaN

        Returns:
            Lista obiektów Cafeteria
        """
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
