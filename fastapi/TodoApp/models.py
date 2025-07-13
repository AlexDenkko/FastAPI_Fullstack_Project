from .database import Base # tämä tuo perusluokan, jota käytetään ORM-mallien kanssa
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey # tuo tarvittavat tietotyypit SQLAlchemy:stä

# tällä luodaan käyttäjien tietokantamalli
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name= Column(String)
    last_name= Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

# Tämä luo todo-alkion tietokantamallin.
class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))