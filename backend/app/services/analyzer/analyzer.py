import pandas as pd
from app.services.recoder.schema import Question
from app.services.analyzer.schema import FrequencieTable, MAQTable, MatrixTable, Crosstable
from app.services.recoder.detector import Detector

class Analyzer:
    def __init__(self, df:pd.DataFrame, mapping:list[Question], crosstables:list[str]):
        self.df = df
        self.mapping:list[Question] = mapping
        self.crosstables = crosstables
        self.tables:list = []
        self.crosstable_tables:list = []
        self.crosstab_df: pd.DataFrame | None = None

    def generate_crosstable(self) -> None:
        for col in self.mapping:
            if col.question is None:
                continue            
            if col.subquestions is not None:
                if col.is_maq:
                    crosstab = self._create_maq_crosstab(col)
                else:
                    for inner_col in col.subquestions:
                        assert inner_col.question is not None
                        counts, combined, percentage  = self._create_crosstab(inner_col)
                        crosstab = Crosstable(
                            cross_table=counts,
                            percentage_table=percentage,
                            combined_table=combined
                        )
                        self.crosstable_tables.append(crosstab)
            else:
                counts, combined, percentage  = self._create_crosstab(col)
                crosstab = Crosstable(
                    cross_table=counts,
                    percentage_table=percentage,
                    combined_table=combined
                )
            self.crosstable_tables.append(crosstab) # type: ignore

    def _create_crosstab(self, question:Question) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        categories = [cafe.value for cafe in question.cafeteria] if question.cafeteria else None
        question_series = pd.Categorical(self.df[question.question], categories) if categories else self.df[question.question]
        sections_counts:list[pd.DataFrame] = []
        sections_percentege:list[pd.DataFrame] = []
        for cross_col in self.crosstables:
            cross_table_counts = pd.crosstab(question_series, self.df[cross_col])
            cross_table_combined = cross_table_counts.copy()
            for col in cross_table_combined.columns:
                cross_table_combined[f'% {col}'] = cross_table_combined[col] / cross_table_combined[col].sum()
            cross_table_percentage = cross_table_combined.copy().drop(columns=[col for col in cross_table_combined.columns if "%" not in col])
            sections_counts.append(cross_table_counts)
            sections_percentege.append(cross_table_percentage)
        counts = pd.concat(sections_counts, axis=1)
        combined = pd.concat(sections_counts + sections_percentege, axis=1)
        percentage = pd.concat(sections_percentege, axis=1)
        return counts, combined, percentage

    def _create_maq_crosstab(
        self,
        col: Question,
    ):
        detector = Detector()
        assert col.cafeteria_dump
        assert col.subquestions
        main_mapping = {cafe["value"]: cafe["index"] for cafe in col.cafeteria_dump}
        subquestions_columns = [subq.question for subq in col.subquestions]
        sections_counts = []
        for cros_col in self.crosstables:
            maq = self.df[subquestions_columns].apply(lambda x: x.map(main_mapping))
            question = []
            for sub_col in subquestions_columns:
                c = pd.crosstab(maq[sub_col].reset_index(name=sub_col).sum(), self.df[cros_col])
                print(c)
                question.append(c)
            q = pd.concat(question, axis=1)
            sections_counts.append(q)


    def create_frequencies_tables(self):
        for col in self.mapping:
            if col.subquestions is None:
                try:
                    question =(pd.Categorical(self.df[col.question], 
                                [unique for unique in self.df[col.question].unique()].sort()) if col.cafeteria is None 
                        else  
                            pd.Categorical(self.df[col.question], 
                                [cafe.value for cafe in col.cafeteria])
                    )
                except:
                    question = self.df[col.question]
                value_count, percentage_table, combined_table = self._create_frequencie_table(question, col)
                table = FrequencieTable(frequncie_table=value_count,
                                                percentage_table=percentage_table,
                                                combined_table=combined_table)
            else:
                if col.is_maq:
                    value_count, percentage_N_table, percentage_QUESTION_table, combined_table = self._create_maq_table(col)
                    table = MAQTable(frequncie_table=value_count,
                                 percentage_N_table=percentage_N_table,
                                 percentage_table=percentage_QUESTION_table,
                                 combined_table=combined_table)
                else:
                    value_count, percentage_table, combined_table = self._create_matrix_counts_table(col)
                    table = MatrixTable(frequncie_table=value_count, 
                                        percentage_table=percentage_table, 
                                        combined_table=combined_table,
                                        subquestions=[])
                    for subquestion in col.subquestions:
                        assert col.cafeteria is not None
                        question = pd.Categorical(self.df[subquestion.question], 
                                [cafe.value for cafe in col.cafeteria])
                        value_count, percentage_table, combined_table = self._create_frequencie_table(question, subquestion)
                        subq = FrequencieTable(frequncie_table=value_count,
                                                percentage_table=percentage_table,
                                                combined_table=combined_table)
                        table.subquestions.append(subq)
            self.tables.append(table)
           

    def _create_frequencie_table(self, question:pd.Series | pd.Categorical | pd.DataFrame, col:Question):
        counts_table = self._calcualate_counts_table(question)
        percentage_table = self._calculate_percentage_table(counts_table.copy(), col)
        combined_table = self._calculate_percentage_table(counts_table.copy(), col)
        return self._add_columnt_tile(counts_table, col), self._add_columnt_tile(percentage_table.drop(columns=["Częstości"]), col), self._add_columnt_tile(combined_table, col)

    def _calcualate_counts_table(self, question:pd.Series | pd.Categorical | pd.DataFrame):
        return question.value_counts().reset_index(name="Częstości")
    
    def _calculate_percentage_table(self, question: pd.DataFrame, col):
        question["% z N"] = question["Częstości"] / col.total_count
        return question

    def _create_matrix_counts_table(self, col:Question):
        matrix = self._assert_matrix_table_sort(col)
        result = self._calcualate_counts_table(matrix.melt())
        percentage_matrix = self._calculate_percentage_table(result.copy(), col)
        combined_matrix = self._calculate_percentage_table(result.copy(), col)
        
        counts_matrix = result.copy().pivot(columns="value", index="variable").fillna(0)
        percentage_matrix =  percentage_matrix.pivot(columns="value", index="variable").fillna(0)
        combined_matrix =  combined_matrix.pivot(columns="value", index="variable").fillna(0)

        counts_matrix.columns = counts_matrix.columns.droplevel(0)
        percentage_matrix.columns = percentage_matrix.columns.droplevel(0)
        combined_matrix.columns = combined_matrix.columns.droplevel(0)
        
        percentage_matrix = percentage_matrix.iloc[:, col.unique_count:].reset_index()
        
        return self._add_columnt_tile(counts_matrix, col), self._add_columnt_tile(percentage_matrix, col), self._add_columnt_tile(combined_matrix, col)

    def _create_maq_table(self, col:Question):
        maq = self._assert_maq_table_sort(col)
        counts_matrix = self._calcualate_maq_counts_table(maq.copy())
        percentage_NSIZE_matrix = self._calcualate_maq_N_percentage_table(counts_matrix.copy(), col)
        percentage_QUESTIONSIZE_matrix = self._calcualate_maq_QUESTION_percentage_table(counts_matrix.copy())
        combined_matrix = self._calcualate_maq_combined_table(counts_matrix, col)
        return (self._add_columnt_tile(counts_matrix, col), self._add_columnt_tile(percentage_NSIZE_matrix,col), 
            self._add_columnt_tile(percentage_QUESTIONSIZE_matrix.drop(columns="Częstości"),col), self._add_columnt_tile(combined_matrix,col))
    
    def _calcualate_maq_combined_table(self, matrix_df:pd.DataFrame, col:Question):
        matrix_df = self._calcualate_maq_N_percentage_table(matrix_df.copy(), col)
        matrix_df = self._calcualate_maq_QUESTION_percentage_table(matrix_df.copy())
        return matrix_df

    def _calcualate_maq_QUESTION_percentage_table(self, matrix_df:pd.DataFrame):
        matrix_df["% z Odpowiedzi"] = (matrix_df["Częstości"] / matrix_df["Częstości"].sum()).round(2)
        return matrix_df

    def _calcualate_maq_N_percentage_table(self, matrix_df:pd.DataFrame, col:Question):
        matrix_df["% z N"] = matrix_df["Częstości"] / col.total_count
        return matrix_df

    def _calcualate_maq_counts_table(self, matrix_df:pd.DataFrame):
        return matrix_df.sum().reset_index(name="Częstości")
    
    def _add_columnt_tile(self, question:pd.DataFrame, col:Question):
        try:
            question.rename(columns={"index": " "})
            question.insert(0, col.question, " ")
        except:
            try:
                question.insert(0, col.question, " ")
            except:
                pass
        return question
    
    def _assert_maq_table_sort(self, col:Question):
            detector = Detector()
            assert col.cafeteria_dump
            assert col.subquestions

            main_mapping = {cafe["value"]:cafe["index"] for cafe in col.cafeteria_dump}
            subquestions_columns = [subq.question for subq in col.subquestions]
            matrix_df = self.df[subquestions_columns]
            matrix_df.columns = [detector.get_cafeteria_item(matrix_col) for matrix_col in matrix_df.columns]
            for column in matrix_df.columns:
                matrix_df[column] = matrix_df[column].map(main_mapping)
            return matrix_df
    
    def _assert_matrix_table_sort(self, col:Question):
        detector = Detector()
        assert col.subquestions is not None
        subquestions_columns = [subq.question for subq in col.subquestions]
        matrix_df:pd.DataFrame = self.df[subquestions_columns]
        matrix_df.columns = [detector.get_cafeteria_item(matrix_col) for matrix_col in matrix_df.columns]
        return matrix_df
