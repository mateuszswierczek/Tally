from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:str | None = None

class User(BaseModel):
    login:str = Field(max_length=32)
    password:str = Field(max_length=32)