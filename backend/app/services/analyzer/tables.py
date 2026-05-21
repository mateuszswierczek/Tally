import pandas as pd
from app.services.recoder.schema import Question
from app.services.analyzer.schema import QuestionTypes
from app.services.recoder.detector import Detector

class FrequenciesTable:
    def __init__(self, df:pd.DataFrame, col:Question, question_type:str = QuestionTypes.orderless):
        self.df = df
        self.col = col
        self.question_type:str = question_type
        self._detector = Detector()
        self.counts_table:pd.DataFrame
        self.percentage_table:pd.DataFrame
        self.combined_table:pd.DataFrame
        self._question:pd.Categorical | pd.DataFrame | pd.Series = self._get_question_type()
        self._compute_na_count()
        self._create_table()

    def _get_question_type(self):
        match self.question_type:
            case QuestionTypes.orderless:
                question = self.df[self.col.question]
            case QuestionTypes.order_by_unique:
                question = pd.Categorical(self.df[self.col.question],[unique for unique in self.df[self.col.question].unique()].sort())
            case QuestionTypes.order_by_mapping:
                assert self.col.cafeteria is not None
                question = pd.Categorical(self.df[self.col.question], [cafe.value for cafe in self.col.cafeteria])
            case QuestionTypes.matrix:
                question = self._assert_matrix_table_sort()
            case QuestionTypes.maq:
                question = self._assert_maq_table_sort()
            case _:
                question = self.df[self.col.question]
        return question

    def _create_table(self):
        question_value_count = self._get_value_count() 
        self.counts_table = question_value_count.copy()
        temp_combined = question_value_count.copy()
        temp_combined["% z N"] = question_value_count["Częstości"] / self.col.total_count
        self.percentage_table = temp_combined.copy().drop(columns=["Częstości"])
        self.combined_table = temp_combined
        if self.question_type == QuestionTypes.matrix:
            self._clean_matrix()

    def _get_value_count(self):
        if self.question_type == QuestionTypes.maq and not isinstance(self._question, pd.Categorical):
            question_value_count = self._question.dropna().sum()
        elif self.question_type == QuestionTypes.matrix and not isinstance(self._question, pd.Categorical):
            question_value_count = self._question.melt().value_counts()
        else:
            question_value_count = self._question.value_counts()
        return question_value_count.reset_index(name="Częstości")    
    
    def _assert_matrix_table_sort(self):
        assert self.col.subquestions is not None
        subquestions_columns = [subq.question for subq in self.col.subquestions]
        matrix_df:pd.DataFrame = self.df[subquestions_columns]
        matrix_df.columns = [self._detector.get_cafeteria_item(matrix_col) for matrix_col in matrix_df.columns]
        print(matrix_df)
        return matrix_df
    
    def _assert_maq_table_sort(self):
        assert self.col.cafeteria_dump
        assert self.col.subquestions

        main_mapping = {cafe["value"]:cafe["index"] for cafe in self.col.cafeteria_dump}
        subquestions_columns = [subq.question for subq in self.col.subquestions]
        matrix_df = self.df[subquestions_columns]
        matrix_df.columns = [self._detector.get_cafeteria_item(matrix_col) for matrix_col in matrix_df.columns]
        for column in matrix_df.columns:
            matrix_df[column] = matrix_df[column].map(main_mapping)
        return matrix_df
    
    def _clean_matrix(self):
            self.counts_table = self.counts_table.pivot(columns="value", index="variable").fillna(0)
            self.counts_table.columns = self.counts_table.columns.droplevel(0)

            self.percentage_table = self.percentage_table.pivot(columns="value", index="variable").fillna(0)
            self.percentage_table.columns = self.percentage_table.columns.droplevel(0)

            self.combined_table = self.combined_table.pivot(columns="value", index="variable").fillna(0)
            self.combined_table.columns = self.combined_table.columns.droplevel(0)
    
    def _compute_na_count(self):
        if isinstance(self._question, pd.DataFrame):
            self.na = self._question.isna().sum()
        else:
            self.na = int(self._question.isna().sum()) 
