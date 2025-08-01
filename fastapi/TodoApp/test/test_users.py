from .utils import * # tuo testausapufunktiot, kuten override_get_db ja override_get_current_user
from TodoApp.routers.users import get_db, get_current_user # tuo get_db ja get_current_user funktiot utils.py tiedostosta
from fastapi import status  # tuo HTTP-tilakoodit, joita käytetään testeissä

app.dependency_overrides[get_db] = override_get_db  # korvaa get_db-funktion testiversiolla
app.dependency_overrides[get_current_user] = override_get_current_user  # korvaa get_current_user-funktion testiversiolla

def test_return_user(test_user):
    response = client.get("/user/")  # tekee GET-pyynnön user-endpointtiin
    assert response.status_code == status.HTTP_200_OK  # tarkistaa, että vastauskoodi on 200 OK
    assert response.json()['username'] == test_user.username  # tarkistaa, että käyttäjänimi on sama kuin testikäyttäjällä
    assert response.json()['email'] == test_user.email  # tarkistaa, että sähköposti on sama kuin testikäyttäjällä
    assert response.json()['first_name'] == test_user.first_name  # tarkistaa, että etunimi on sama kuin testikäyttäjällä
    assert response.json()['last_name'] == test_user.last_name  # tarkistaa, että sukunimi on sama kuin testikäyttäjällä
    assert response.json()['role'] == test_user.role  # tarkistaa, että rooli on sama kuin testikäyttäjällä