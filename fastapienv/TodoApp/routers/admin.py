from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(    
    prefix="/admin",
    tags=["admin"]
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
user_dependency = Annotated[dict, Depends(get_current_user)]
# Tämä määrittelee reitit, jotka liittyvät admin-toimintoihin.


@router.get("/todo", status_code=200)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).all()
# Tämä endpoint palauttaa kaikki todo-tietueet tietokannasta jos olet sisäänkirjautunut / oikeutettu.


@router.delete("/todo/{todo_id}", status_code=204)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()