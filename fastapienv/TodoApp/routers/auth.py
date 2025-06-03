from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from passlib.context import CryptContext #Tuodaan bcryptin käyttöön passlib-kirjastosta
from fastapi.security import OAuth2PasswordRequestForm #Tuodaan OAuth2PasswordRequestForm, jota käytetään kirjautumiseen
from jose import jwt
router = APIRouter()

SECRET_KEY = 'a49b24820ae3658dfea66bce4cadd2b520d92b64c0322dce4318d7c81b4cf18e'
ALGORITHM = 'HS256'
# Tämä on salainen avain, jota käytetään JWT-tunnusten allekirjoittamiseen. 
# openssl rand -hex 32 komennolla voi luoda uuden salaisen avaimen.

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Tämä määrittelee bcryptin käytön salasanan hashaukseen.

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
# Tämä luokka määrittelee käyttäjän luomisen vaatimukset.

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Tämä funktio luo tietokantayhteyden ja sulkee sen lopuksi.
# Se käyttää SessionLocal luokkaa, joka on määritelty database.py tiedostossa.

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user
# Tämä funktio tarkistaa käyttäjän todennuksen.

def create_access_token(username:str, user_id:int, expires_delta: timedelta):

    encode = {
        "sub": username,
        "id": user_id,
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# Luodaan CreateUserRequest luokka, joka määrittelee käyttäjän luomisen vaatimukset.
@router.post("/auth", status_code=201)
async def create_user(db: db_dependency, 
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role= create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password), #Hashataan salasana bcryptillä
        is_active=True
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed Authentication'
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
# Tämä reitti käsittelee kirjautumisen ja palauttaa viestin onnistuneesta tai epäonnistuneesta todennuksesta.