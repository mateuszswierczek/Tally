from pydantic import BaseModel
from enum import StrEnum
from typing import Literal 

class QuestionType(StrEnum):
    """Poziom zmiennej w sensie statystycznym."""
    single = "Pojedyńczy wybór"
    maq = "Wielokrotnego wyboru"
    text = "Otwarte"
    table = "Tabela"

class SurveyQuestion(BaseModel):
    text: str
    index: int
    question_type: Literal["Pojedyńczy wybór", "Wielokrotnego wyboru", "Otwarte", "Tabela"]
    cafeteria: list['SurveyCafeteria']
    is_showable: bool

class SurveyTable(SurveyQuestion):
    columns: list['SurveyCafeteria']

class SurveyCafeteria(BaseModel):
    item: str
    index: int