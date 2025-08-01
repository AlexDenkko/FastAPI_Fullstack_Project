from .utils import * # tuo kaikki funktiot utils.py tiedostosta
from TodoApp.routers.admin import get_db, get_current_user # tuo get_db ja get_current_user funktiot utils.py tiedostosta
from fastapi import status # tuo HTTP-tilakoodit, joita käytetään testeissä

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