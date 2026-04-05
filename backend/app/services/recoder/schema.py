from pydantic import BaseModel
from typing import Literal 
from enum import StrEnum

class ColumnType(StrEnum):
    """Poziom zmiennej w sensie statystycznym."""
    ordinal = "ordinal"
    nominal = "nominal"
    continuous = "continuous"
    text = "text"

class Question(BaseModel):
    """Pojedyńcze pytanie ankiety."""
    question: str | None
    index: int | None
    type: Literal["ordinal", "nominal", "continuous", "text"]
    unique_count: int | None
    missing_count: int | None
    total_count: int
    ignored: bool = False
    cafeteria: list['Cafeteria'] | None = None
    cafeteria_dump: list[dict] | None = None
    subquestions: list['Question'] | None = None

class Cafeteria(BaseModel):
    """Pojedyncza odpowiedź w kafeterii pytania."""
    value: str | None = None
    index: int | None = None
    n: int | None = None
    pct: float | None = None
    is_missing: bool = False
    missing_code: str | int | None = None

class Mapping(BaseModel):
    question: str | None
    index: int | None
    type: Literal["ordinal", "nominal", "continuous", "text"]
    unique_count: int | None
    missing_count: int | None
    total_count: int | None
    ignored: bool = False
    cafeteria: list | None = None
    cafeteria_dump: list | None = None
    subquestions: list | None = None