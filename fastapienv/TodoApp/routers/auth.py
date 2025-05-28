from fastapi import APIRouter
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext #Tuodaan bcryptin käyttöön passlib-kirjastosta

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Tämä määrittelee bcryptin käytön salasanan hashaukseen.

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
# Tämä luokka määrittelee käyttäjän luomisen vaatimukset.


# Luodaan CreateUserRequest luokka, joka määrittelee käyttäjän luomisen vaatimukset.
@router.post("/auth")
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role= create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password), #Hashataan salasana bcryptillä
        is_active=True
    )

    return create_user_model


    return {"user": "authenticated"}