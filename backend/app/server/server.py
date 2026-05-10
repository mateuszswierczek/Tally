# TODO - ARCHITEKTURA:
# [ ] Baza
# [ ] Hashowanie haseł (passlib)
# [ ] CONSTANTS do zmiennych środowiskowych
# [ ] Podłączyć TokenData
# [ ] Chronione endpointy
# [ ] Obsługa wygaśnięcia tokena — refresh token
# [ ] Walidacja danych wejściowych
# [ ] Pooling rate
# [ ] SlowAPI
# [ ] Po dodaniu hashowania: Przy sprawdzaniu usera, gdy usera nie ma w bazie, 
# 'sprawdzić' hasło na DummyHash

# TODO - PÓŹNIEJ:
# [ ] Logowanie requestów
# [ ] Testy jednostkowe dla authenticate_user i create_access_token

from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from models import User, Token, TokenData, MappingPayload, MappingDocxPayload
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from typing import Annotated
from app.services.recoder.recoder import Recoder
from app.services.recoder.exporter import write_to_excel
from app.services.recoder.mapper import Mapper
from app.services.analyzer.analyzer import Analyzer
from app.services.surveyParser.parser import QuestionnaireParser
from app.services.surveyParser.lime_parser import LimeParser
from file_sanitizer import sanitize_excel_file
from io import BytesIO

import dotenv
import jwt
import os

dotenv.load_dotenv()

ORIGINS = [
"https://backend-production-6afc.up.railway.app/",
"http://localhost:3001",
"https://localhost:3001"
]
ACCESS_TOKEN_EXPIRES:int = 300
SECRET = "gasd23j5rthn2qtgfkadsjnjk324"
ALGORITHM = "HS256"
MAX_FILE_SIZE = 10 * 1024 * 1024 #10 MB
ADMIN_USER = os.environ["USERNAME"]
ADMIN_PASSWORD = os.environ["PASSWORD"]

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins = ORIGINS,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def create_acces_token(data:dict, expires_time:timedelta = timedelta(minutes=30)):
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + expires_time
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def get_user(username:str, db = None):
    if username == ADMIN_USER:
        return "admin"

def authenticate_user(login, password, db=None):
    user = get_user(login)
    if not user:
        return False
    if password == ADMIN_PASSWORD:
        return True
    return False

def set_recoder(content:BytesIO, filename:str) -> None: 
    global recoder
    recoder = Recoder(content, filename)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate credentails",
        headers={"WWW-authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        #token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/health")
async def health():
    return {"status":"healthy"}

@app.post("/api/auth_user")
async def auth_users_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if user == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Błędne hasło lub login.",
            headers={"WWW-authenticate":"Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES)
    access_token = create_acces_token(data={"sub":form_data.username}, 
                                      expires_time=access_token_expires)
    return Token(access_token=access_token, 
                 token_type="bearer")

@app.post("/api/post_excel")
async def receive_excel_file(file: UploadFile = File(...), _= Depends(get_current_user)):
    await sanitize_excel_file(file)
    content = await file.read()
    assert file.filename is not None
    set_recoder(BytesIO(content), file.filename)
    recoder.parser.iterate()
    return {"mapping":recoder.parser.mapping_data}

@app.post("/api/post_mapping")
async def receive_mapping(payload:MappingPayload, _= Depends(get_current_user)):
    mapping = payload.mapping
    crosstables = payload.crosstables
    merged = payload.merged
    analyzer = Analyzer(recoder.df, mapping, crosstables)
    mapper = Mapper(recoder.df)
    mapped_df = mapper.map_coding_onto_database(mapping, mapper.df)
    book_of_codes = mapper.create_book_of_codes(mapping)
    ziped_files = write_to_excel(analyzer, 
                                    mapper.df, 
                                    mapped_df, 
                                    mapping, 
                                    book_of_codes)
    return StreamingResponse(ziped_files, 
                            200, 
                            media_type="application/zip",
                            headers={"Content-Disposition": "attachment; filename=Baza danych.zip"})

@app.post("/api/post_questionnaire")
async def receive_questionnaire(file:UploadFile = File(...), _=Depends(get_current_user)):
    content = await file.read()
    survey_parser = QuestionnaireParser(BytesIO(content))
    questionnaire_mapping = survey_parser.parser_questionnaire_instrument()
    return {"mapping":questionnaire_mapping}

@app.post("/api/post_docx_mapping")
async def receive_docx_mapping(payload:MappingDocxPayload, _= Depends(get_current_user)):
    mapping = payload.mapping
    lime_parser = LimeParser(mapping)
    lime_parser.create_questionnaire()