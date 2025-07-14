from sqlalchemy import create_engine # tuo SQLAlchemy:n create_engine-funktion, joka luo tietokantamoottorin
from sqlalchemy.pool import StaticPool # tuo staattisen poolin, joka on hyödyllinen testauksessa
from sqlalchemy.orm import sessionmaker # tuo sessionmaker, jota käytetään tietokantayhteyksien hallintaan
from TodoApp.database import Base # tuo Base-luokan, jota käytetään ORM-mallien kanssa
from TodoApp.main import app # tuo pääsovelluksen, joka on määritelty main.py-tiedostossa
from TodoApp.routers.todos import get_db, get_current_user # tuo tietokantayhteyden ja käyttäjän hakufunktiot
from fastapi.testclient import TestClient # tuo FastAPI:n testausasiakkaan, jota käytetään testauksessa
from fastapi import status # tuo HTTP-tilakoodit, joita käytetään testeissä

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

def test_read_all_authenticated():
    response = client.get("/") # tekee GET-pyynnön todos-endpointtiin
    assert response.status_code == status.HTTP_200_OK # tarkistaa, että vastauskoodi on 200 OK
    assert isinstance(response.json(), list) # tarkistaa, että vastaus on lista
