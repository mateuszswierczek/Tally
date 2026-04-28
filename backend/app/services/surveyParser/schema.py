from pydantic import BaseModel
from enum import StrEnum
from typing import Literal 

class QuestionType(StrEnum):
    single = "single"
    maq = "maq"
    text = "text"
    table = "table"
    numerical = "numerical"

class SurveyQuestion(BaseModel):
    text: str
    index: int
    #TODO: Zamienić na list iter
    question_type: Literal["single", "maq", "text", "table", "numerical"]
    cafeteria: list['SurveyCafeteria']
    is_showable: bool

class SurveyTable(SurveyQuestion):
    columns: list['SurveyCafeteria']

class SurveyCafeteria(BaseModel):
    item: str | int
    index: int