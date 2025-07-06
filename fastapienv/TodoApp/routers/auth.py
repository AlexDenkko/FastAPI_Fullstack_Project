from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from passlib.context import CryptContext #Tuodaan bcryptin käyttöön passlib-kirjastosta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer #Tuodaan OAuth2PasswordRequestForm, jota käytetään kirjautumiseen
from jose import jwt, JWTError

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
# Tämä määrittelee reitit, jotka liittyvät käyttäjän todennukseen ja JWT-tunnusten luomiseen.

SECRET_KEY = 'a49b24820ae3658dfea66bce4cadd2b520d92b64c0322dce4318d7c81b4cf18e'
ALGORITHM = 'HS256'
# Tämä on salainen avain, jota käytetään JWT-tunnusten allekirjoittamiseen. 
# openssl rand -hex 32 komennolla voi luoda uuden salaisen avaimen.

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Tämä määrittelee bcryptin käytön salasanan hashaukseen.
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
# Tämä määrittelee OAuth2-todennuksen ja tokenUrl:n, jota käytetään kirjautumiseen.

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
    # Tämä luokka määrittelee JWT-tunnuksen rakenteen, joka palautetaan kirjautumisen yhteydessä.

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

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):

    encode = {
        "sub": username,
        "id": user_id,
        "role": role
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
# Tämä funktio luo JWT-tunnuksen käyttäjälle.


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Could not validate user.')


# Luodaan CreateUserRequest luokka, joka määrittelee käyttäjän luomisen vaatimukset.
@router.post("/", status_code=201)
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
    # Tämä endpoint luo uuden käyttäjän tietokantaan.


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Could not validate user.')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
# Tämä reitti käsittelee kirjautumisen ja palauttaa viestin onnistuneesta tai epäonnistuneesta todennuksesta.