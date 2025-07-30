from sqlalchemy import create_engine, text # tuo SQLAlchemy:n create_engine-funktion, joka luo tietokantamoottorin
from sqlalchemy.pool import StaticPool # tuo staattisen poolin, joka on hyödyllinen testauksessa
from sqlalchemy.orm import sessionmaker, declarative_base # tuo sessionmaker, jota käytetään tietokantayhteyksien hallintaan ja declarative_base, joka luo perusluokan, jota käytetään ORM-mallien kanssa
from TodoApp.main import app # tuo pääsovelluksen, joka on määritelty main.py-tiedostossa
from TodoApp.routers.todos import get_db, get_current_user # tuo tietokantayhteyden ja käyttäjän hakufunktiot
from fastapi.testclient import TestClient # tuo FastAPI:n testausasiakkaan, jota käytetään testauksessa
from fastapi import status # tuo HTTP-tilakoodit, joita käytetään testeissä
import pytest # tuo pytest-kirjaston, jota käytetään testauksen hallintaan
from TodoApp.models import Todos
from TodoApp.database import Base  # Add this line to import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" # määrittelee SQLite-tietokannan osoitteen

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  # määrittelee tietokannan osoitteen
    connect_args={"check_same_thread": False}, # SQLite vaatii tämän argumentin monisäikeisessä käytössä
    poolclass= StaticPool, # käyttää staattista poolia, joka on hyödyllinen testauksessa
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # luo session, jota käytetään testauksessa


Base.metadata.create_all(bind=engine) # luo kaikki taulut tietokantaan, jotka on määritelty Base-luokan perijöissä
# Tämä on hyödyllistä testauksessa, jotta voidaan varmistaa, että tietokanta on valmis testejä varten.

def override_get_db():
    db = TestingSessionLocal() # luo uuden session testauksessa
    try:
        yield db # palauttaa session, jota voidaan käyttää testeissä
    finally:
        db.close() # sulkee session testauksen jälkeen

def override_get_current_user():
    return {'username': 'admintest', 'id': 1, 'user_role': 'admin'} # palauttaa testikäyttäjän, jota voidaan käyttää testeissä

app.dependency_overrides[get_db] = override_get_db # korvaa get_db-funktion testiversiolla, jotta testit voivat käyttää testitietokantaa
app.dependency_overrides[get_current_user] = override_get_current_user # korvaa get_current_user-funktion testiversiolla, jotta testit voivat käyttää testikäyttäjää

client = TestClient(app) # luo testausasiakkaan pääsovellukselle, jota voidaan käyttää testeissä

@pytest.fixture # määrittelee testitietokannan todos-tietueen
def test_todo(): 
    todo = Todos( # luo uuden Todos-tietueen testitietokantaa varten
        title= "Learn to code!",
        description= "Need to learn everyday!",
        priority= 5,
        complete= False,
        owner_id= 1,
    )

    db = TestingSessionLocal()  # TÄRKEÄ! KÄYTÄ VAIN TESTI TIETOKANTAA MUUTEN TÄMÄ YLIKIRJOITTAA OIKEETA TIETOKANTAA
    # luo uuden session testitietokantaa varten
    db.add(todo) # lisää testitodo-tietueen tietokantaan
    db.commit()     # sitoo muutokset tietokantaan
    yield todo  # palauttaa testitodo-tietueen, jota voidaan käyttää testeissä
    with engine.connect() as connection:
        connection.execute(text("DELETE From todos;"))  # Tyhjentää testitietokannan todos-taulun
        connection.commit()

def test_read_all_authenticated(test_todo: Todos):  
    response = client.get("/") # tekee GET-pyynnön todos-endpointtiin
    assert response.status_code == status.HTTP_200_OK # tarkistaa, että vastauskoodi on 200 OK
    assert response.json() == [{
        'id': test_todo.id,  # include the id field
        'complete': False,
        'title': 'Learn to code!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'owner_id': 1
    }] # tarkistaa, että vastaus on lista

def test_read_one_authenticated(test_todo):  
    response = client.get("/todo/1") # tekee GET-pyynnön todos-endpointtiin
    assert response.status_code == status.HTTP_200_OK # tarkistaa, että vastauskoodi on 200 OK
    assert response.json() == {
        'id': 1,  
        'complete': False,
        'title': 'Learn to code!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'owner_id': 1
    } # tarkistaa, että vastaus on lista

def test_read_one_authenticated_not_found(test_todo):  
    response = client.get("/todo/999") # tekee GET-pyynnön todos-endpointtiin
    assert response.status_code == status.HTTP_404_NOT_FOUND # tarkistaa, että vastauskoodi on 404 NOT FOUND
    assert response.json() == {'detail': 'Todo not found'} # tarkistaa, että vastaus on lista


def test_create_todo(test_todo):
    request_data = {
        'title': 'New Todo',
        'description': 'This is a new todo description.',
        'priority': 5,
        'complete': False
    }

    response = client.post('/todo/', json=request_data) # tekee POST-pyynnön todos-endpointtiin
    assert response.status_code == 201 # tarkistaa, että vastauskoodi on 201 CREATED

    db = TestingSessionLocal()  # luo uuden session testitietokantaa varten
    model = db.query(Todos).filter(Todos.id == 2).first()  # hakee juuri luodun Todos-tietueen testitietokannasta
    assert model.title == request_data.get('title')  # tarkistaa, että otsikko on sama kuin pyynnössä
    assert model.description == request_data.get('description')  # tarkistaa, että kuvaus on sama kuin pyynnössä
    assert model.priority == request_data.get('priority')  # tarkistaa, että prioriteetti on sama kuin pyynnössä
    assert model.complete == request_data.get('complete')  # tarkistaa, että valmis on sama kuin pyynnössä


def test_update_todo(test_todo):
    request_data = {
        'title': 'Change the title of prompt already saved',
        'description': 'Need to learn this.',
        'priority': 5,
        'complete': False,
    }

    response = client.put('/todo/1', json=request_data) # tekee PUT-pyynnön todos-endpointtiin
    assert response.status_code == status.HTTP_204_NO_CONTENT # tarkistaa, että vastauskoodi on 204 NO CONTENT

    db = TestingSessionLocal()  # luo uuden session testitietokantaa varten
    model = db.query(Todos).filter(Todos.id == 1).first()  # hakee juuri päivitetyn Todos-tietueen testitietokannasta
    assert model.title == 'Change the title of prompt already saved'  # tarkistaa, että otsikko on sama kuin pyynnössä

def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'Change the title of prompt already saved',
        'description': 'Need to learn this.',
        'priority': 5,
        'complete': False,
    }

    response = client.put('/todo/999', json=request_data) # tekee PUT-pyynnön todos-endpointtiin
    assert response.status_code == 404 # tarkistaa, että vastauskoodi on 404 NOT FOUND
    assert response.json() == {'detail': 'Todo not found.'} # tarkistaa, että vastaus on lista


def test_delete_todo(test_todo):
    response = client.delete('/todo/1') # tekee DELETE-pyynnön todos-endpointtiin
    assert response.status_code == status.HTTP_204_NO_CONTENT # tarkistaa, että vastauskoodi on 204 NO CONTENT

    db = TestingSessionLocal()  # luo uuden session testitietokantaa varten
    model = db.query(Todos).filter(Todos.id == 1).first()  # hakee juuri poistettu Todos-tietueen testitietokannasta
    assert model is None  # tarkistaa, että tietuetta ei ole enää olemassa


def test_delete_todo_not_found(test_todo):
    response = client.delete('/todo/999') # tekee DELETE-pyynnön todos-endpointtiin
    assert response.status_code == 404 # tarkistaa, että vastauskoodi on 404 NOT FOUND
    assert response.json() == {'detail': 'Todo not found.'} # tarkistaa, että vastaus on lista