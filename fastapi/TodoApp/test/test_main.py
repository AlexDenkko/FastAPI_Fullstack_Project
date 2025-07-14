from fastapi.testclient import TestClient # tämä tuo FastAPI:n testausasiakkaan
from TodoApp.main import app # tuo TodoAppin pääsovelluksen
from fastapi import status # tämä tuo HTTP-tilakoodit


client = TestClient(app) # luo testausasiakkaan pääsovellukselle

def test_health_check(): # testaa terveystarkistusta
    response = client.get("/healthy") # tekee GET-pyynnön terveystarkistukseen
    assert response.status_code == status.HTTP_200_OK # tarkistaa, että vastauskoodi on 200 OK
    assert response.json() == {"status": "healthy"} # tarkistaa, että vastaus on odotettu JSON-objekti