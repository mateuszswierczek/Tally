from pydantic import BaseModel, ConfigDict
import pandas as pd

class FrequencieTable(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)   

    frequncie_table:pd.DataFrame
    percentage_table:pd.DataFrame
    combined_table:pd.DataFrame

class MAQTable(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)   

    frequncie_table:pd.DataFrame
    percentage_N_table:pd.DataFrame
    percentage_QUESTION_table:pd.DataFrame
    combined_table:pd.DataFrame

class MatrixTable(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)   

    frequncie_table:pd.DataFrame
    percentage_table:pd.DataFrame
    combined_table:pd.DataFrame
    subquestions:list['FrequencieTable']