from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from passlib.context import CryptContext #Tuodaan bcryptin käyttöön passlib-kirjastosta

router = APIRouter()

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Tämä funktio luo tietokantayhteyden ja sulkee sen lopuksi.
# Se käyttää SessionLocal luokkaa, joka on määritelty database.py tiedostossa.

db_dependency = Annotated[Session, Depends(get_db)]



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


