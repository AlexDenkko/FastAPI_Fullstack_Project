from TodoApp.models import Users
from .utils import *
from TodoApp.routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import timedelta

app.dependency_overrides[get_db] = override_get_db # korvaa get_db-funktion testiversiolla

def test_authenticate_user(test_user: Users):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, 'testpassword', db)
    assert authenticated_user is not None  # tarkistaa, että käyttäjä on autentikoitu
    assert authenticated_user.username == test_user.username  # tarkistaa, että käyttäjänimi on sama kuin testikäyttäjällä

    non_existent_user = authenticate_user('WrongUsername', 'wrongpassword', db)
    assert non_existent_user is False  # tarkistaa, että ei-autentikoitu käyttäjä on False 

    wrong_password_user = authenticate_user(test_user.username, 'wrongpassword', db)
    assert wrong_password_user is False  # tarkistaa, että väärällä salasanalla autentikointi epäonnistuu


def test_create_access_token(test_user: Users): 
    username = 'testuser' 
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1) # määrittää tokenin voimassaolon ajan

    token = create_access_token(username, user_id, role, expires_delta) # luo access tokenin

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], # varmista, että token on dekoodattu oikein
                               options={"verify_signature": False}) # "älä varmista" allekirjoitusta testauksen aikana koska se ei ole tarpeen

    assert decoded_token['sub'] == username  # tarkistaa, että käyttäjänimi on sama kuin tokenissa
    assert decoded_token['id'] == user_id  # tarkistaa, että käyttäjän ID on sama kuin tokenissa
    assert decoded_token['role'] == role  # tarkistaa, että roolit ovat samat kuin tokenissa