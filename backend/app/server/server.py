# TODO - ARCHITEKTURA:
# [ ] Prawdziwa baza danych zamiast fake_db = ["admin"]
# [ ] Hashowanie haseł (np. bcrypt / passlib) — nigdy plaintext
# [ ] SECRET do zmiennej środowiskowej (.env + python-dotenv)
# [ ] Odkomentować i podłączyć TokenData — jest zaimportowany, ale nieużywany
# [ ] Przynajmniej jeden przykładowy chroniony endpoint (np. GET /api/me)
# [ ] Obsługa wygaśnięcia tokena — refresh token lub odpowiedni komunikat błędu
# [ ] Walidacja danych wejściowych

# TODO - OPCJONALNIE:
# [ ] Logowanie requestów
# [ ] Testy jednostkowe dla authenticate_user i create_access_token

from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status
from models import User, Token, TokenData
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt

app = FastAPI()

origins = [
"http://localhost:3001",
"https://localhost:3001"
]

ACCESS_TOKEN_EXPIRES:int = 30
SECRET = "gasd23j5rthn2qtgfkadsjnjk324"
ALGORITHM = "HS256"

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
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

@app.get("/health")
async def health():
    return {"status":"healthy"}

@app.post("/api/auth_user")
async def auth_users_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    print(form_data)
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