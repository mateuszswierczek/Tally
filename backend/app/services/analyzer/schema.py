from pydantic import BaseModel, ConfigDict
from enum import StrEnum
import pandas as pd

class QuestionTypes(StrEnum):
    orderless = "Orderless"
    order_by_unique = "Unique"
    order_by_mapping = "Mapped"
    matrix = "Matrix"
    maq = "MAQ"

class FrequencieTable(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)   

    frequncie_table:pd.DataFrame
    percentage_table:pd.DataFrame
    combined_table:pd.DataFrame

class MAQTable(FrequencieTable):
    model_config = ConfigDict(arbitrary_types_allowed=True)   

    percentage_N_table:pd.DataFrame

class MatrixTable(FrequencieTable):
    model_config = ConfigDict(arbitrary_types_allowed=True)   

    subquestions:list['FrequencieTable']

class Crosstable(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)   

    cross_table:pd.DataFrame
    percentage_table:pd.DataFrame
    combined_table:pd.DataFrame   