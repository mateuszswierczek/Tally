from pydantic import BaseModel
from enum import StrEnum
from typing import Literal 

class QuestionType(StrEnum):
    """Poziom zmiennej w sensie statystycznym."""
    single = "Pojedyńczy wybór"
    maq = "Wielokrotnego wyboru"
    text = "Tekstowa"
    table = "Tabela"
    numerical = "Numeryczna"

class SurveyQuestion(BaseModel):
    text: str
    index: int
    #TODO: Zamienić na list iter
    question_type: Literal["Pojedyńczy wybór", "Wielokrotnego wyboru", "Tekstowa", "Tabela", "Numeryczna"]
    cafeteria: list['SurveyCafeteria']
    is_showable: bool

class SurveyTable(SurveyQuestion):
    columns: list['SurveyCafeteria']

class SurveyCafeteria(BaseModel):
    item: str | int
    index: int