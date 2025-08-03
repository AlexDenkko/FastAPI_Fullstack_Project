from .utils import *
from TodoApp.routers.auth import get_db, authenticate_user

app.dependency_overrides[get_db] = override_get_db # korvaa get_db-funktion testiversiolla

def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, 'testpassword', db)
    assert authenticated_user is not None  # tarkistaa, että käyttäjä on autentikoitu
    assert authenticated_user.username == test_user.username  # tarkistaa, että käyttäjänimi on sama kuin testikäyttäjällä

    non_existent_user = authenticate_user('WrongUsername', 'wrongpassword', db)
    assert non_existent_user is False  # tarkistaa, että ei-autentikoitu käyttäjä on False 

    wrong_password_user = authenticate_user(test_user.username, 'wrongpassword', db)
    assert wrong_password_user is False  # tarkistaa, että väärällä salasanalla autentikointi epäonnistuu
