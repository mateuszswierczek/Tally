from pydantic import BaseModel, ConfigDict
import pandas as pd

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