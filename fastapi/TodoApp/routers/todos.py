from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, status
from ..models import Todos
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter()
# Tämä määrittelee reitit, jotka liittyvät käyttäjän toimintoihin.

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

class TodoRequest(BaseModel):
    priority: int = Field(gt=0, lt=6)
    complete: bool
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
# Tämä luokka määrittelee vaatimukset.


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    #tarkistetaan, että käyttäjä on kirjautunut sisään
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all() 
# Tämä endpoint palauttaa kaikki todo-tietueet tietokannasta jos olet sisäänkirjautunut / oikeutettu.

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
# Tämä endpoint palauttaa yksittäisen todo-tietueen tietokannasta jos olet sisäänkirjautunut / oikeutettu.

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, 
                      todo_request: TodoRequest):
    #tarkistetaan, että käyttäjä on kirjautunut sisään
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
        #tarkistetaan, että käyttäjä on kirjautunut sisään
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    

    db.add(todo_model)
    db.commit()
# Tämä endpoint luo uuden todo-tietueen tietokantaan.


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    #tarkistetaan, että käyttäjä on kirjautunut sisään
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found.')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()
# Tämä endpoint päivittää olemassa olevan todo-tietueen tietokannassa.

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()

    db.commit()
# Tämä endpoint poistaa todo-tietueen tietokannasta.