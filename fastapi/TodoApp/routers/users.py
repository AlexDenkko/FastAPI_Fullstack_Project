from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from ..models import Todos, Users
from ..database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix="/user",
    tags=["user"]
    #Tässä määritellään reitit, jotka liittyvät käyttäjän toimintoihin.
)

#Tässä tiedostossa luodaan endpointit todo-sovellukselle.
#Tämä tiedosto on tarkoitettu todo-sovelluksen toiminnallisuuksien toteuttamiseen.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Tämä funktio luo tietokantayhteyden ja sulkee sen lopuksi.
# Se käyttää SessionLocal luokkaa, joka on määritelty database.py tiedostossa.

        
db_dependency = Annotated[Session, Depends(get_db)]
# Tämä määrittelee tietokantayhteyden riippuvuuden, jota käytetään reiteissä.
user_dependency = Annotated[dict, Depends(get_current_user)]
# Tämä määrittelee reitit, jotka liittyvät käyttäjän toimintoihin.
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Tämä määrittelee bcryptin käytön salasanan hashaukseen.

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length= 6)
    # Tämä luokka määrittelee käyttäjän vahvistuksen vaatimukset, kuten nykyisen salasanan ja uuden salasanan.


@router.get("/", status_code=200)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Users).filter(Users.id == user.get('id')).first()
# Tämä endpoint palauttaa käyttäjän tiedot tietokannasta jos olet sisäänkirjautunut / oikeutettu.

@router.put("/password", status_code=204)
async def change_password(user: user_dependency, db: db_dependency, 
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=403, detail="Error on password change")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
