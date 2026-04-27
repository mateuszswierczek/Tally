from pydantic import BaseModel, Field
from app.services.recoder.schema import Question
from app.services.surveyParser.schema import SurveyQuestion

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:str | None = None

class User(BaseModel):
    login:str = Field(max_length=32)
    password:str = Field(max_length=32)

class MappingPayload(BaseModel):
    mapping: list[Question]
    crosstables: list[str]

class MappingDocxPayload(BaseModel):
    mapping: list[SurveyQuestion]