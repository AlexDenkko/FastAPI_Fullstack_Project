from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos
from database import SessionLocal

router = APIRouter()

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

class TodoRequest(BaseModel):
    priority: int = Field(gt=0, lt=6)
    complete: bool
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
# Tämä luokka määrittelee vaatimukset.


@router.get("/", status_code=200)
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(Todos).all()
# Tämä endpoint palauttaa kaikki todo-tietueet tietokannasta.

@router.get("/{todo_id}", status_code=200)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")
# Tämä endpoint palauttaa yksittäisen todo-tietueen tietokannasta.

@router.post("/todo", status_code=201)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()
# Tämä endpoint luo uuden todo-tietueen tietokantaan.


@router.put("/todo/{todo_id}", status_code=204)
async def update_todo(db: db_dependency,
                      todo_id:int,
                      todo_request: TodoRequest):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()
# Tämä endpoint päivittää olemassa olevan todo-tietueen tietokannassa.

@router.delete("/todo/{todo_id}", status_code=204)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()
# Tämä endpoint poistaa todo-tietueen tietokannasta.