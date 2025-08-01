from .utils import * # tuo kaikki funktiot utils.py tiedostosta
from TodoApp.routers.admin import get_db, get_current_user # tuo get_db ja get_current_user funktiot utils.py tiedostosta
from fastapi import status # tuo HTTP-tilakoodit, joita käytetään testeissä
from TodoApp.models import Todos # tuo Todos-malli, jota käytetään testeissä

app.dependency_overrides[get_db] = override_get_db # korvaa get_db-funktion testiversiolla
app.dependency_overrides[get_current_user] = override_get_current_user # korvaa get_current_user-funktion testiversiolla

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo") # tekee GET-pyynnön admin-todo-endpointtiin
    assert response.status_code == status.HTTP_200_OK # tarkistaa, että vastauskoodi on 200 OK
    assert response.json() == [{
        'id': test_todo.id,  # sisältää id-kentän
        'complete': False,
        'title': 'Learn to code!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'owner_id': 1
    }] # tarkistaa, että vastaus on lista


def test_admin_delete_todo(test_todo): # tekee DELETE-pyynnön admin-todo-endpointtiin
    response = client.delete(f"/admin/todo/1") # tekee DELETE-pyynnön admin-todo-endpointtiin
    assert response.status_code == status.HTTP_204_NO_CONTENT # tarkistaa, että vastauskoodi on 204 NO CONTENT

    db = TestingSessionLocal()  # luo uuden session testitietokantaa varten
    model = db.query(Todos).filter(Todos.id == 1).first()  # hakee juuri luodun Todos-tietueen testitietokannasta
    assert model is None 


def test_admin_delete_todo_not_found(): # (testi jos ei löydy) # Tämä testi tarkistaa, että jos yritetään poistaa todoa, jota ei ole olemassa, saadaan 404 NOT FOUND
    response = client.delete(f"/admin/todo/999") # tekee DELETE-pyynnön admin-todo-endpointtiin
    assert response.status_code == status.HTTP_404_NOT_FOUND # tarkistaa, että vastauskoodi on 404 NOT FOUND
    assert response.json() == {'detail': 'Todo not found'} # tarkistaa, että vastaus on lista
