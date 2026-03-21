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
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from models import User, Token, TokenData
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from typing import Annotated
from app.services.recoder.recoder import Recoder
from file_sanitizer import sanitize_excel_file
from io import BytesIO


import logging
import jwt


#app/services/recoder/recoder.py
#####################################################################
# CONSTANTS
#####################################################################
ORIGINS = [
"http://localhost:3001",
"https://localhost:3001"
]
ACCESS_TOKEN_EXPIRES:int = 30
SECRET = "gasd23j5rthn2qtgfkadsjnjk324"
ALGORITHM = "HS256"
MAX_FILE_SIZE = 10 * 1024 * 1024 #10 MB

#####################################################################
# SERVER SET-UP
#####################################################################
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ORIGINS,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

#####################################################################
# HELPER FUNCTIONS
#####################################################################

def create_acces_token(data:dict, expires_time:timedelta = timedelta(minutes=30)):
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + expires_time
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def get_user(username:str, db = None):
    fake_db = ["admin"]
    if username in fake_db:
        return "admin"

def authenticate_user(login, password, db=None):
    user = get_user(login)
    if not user:
        return False
    fake_pass = "test123"
    if password == fake_pass:
        return True
    return False

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

#####################################################################
# ENDPOINTS
#####################################################################
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
    recoder = Recoder(BytesIO(content), file.filename)
    recoder.parser.iterate()
    mapping = recoder.parser._grouped_data
    return {"mapping":mapping}