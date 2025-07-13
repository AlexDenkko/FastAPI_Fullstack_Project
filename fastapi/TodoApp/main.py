from fastapi import FastAPI # tämä tuo FastAPI-sovelluskehyksen
from .models import Base # tämä tuo mallit, jotka määrittelevät tietokannan rakenteen
from .database import engine # tämä tuo moottorin tietokantayhteyttä varten
from .routers import auth, todos, admin, users # tämä tuo reitittimet eri toiminnallisuuksia varten

app = FastAPI()

Base.metadata.create_all(bind=engine)
# Luo kaikki taulut tietokannassa, jotka on määritelty malleissa

@app.get("/healthy")
def health_check():
    return {"status": "healthy"}
# tämä on terveystarkistus, joka palauttaa terveen tilan

app.include_router(auth.router) # tämä tuo autentikointireitittimen
app.include_router(todos.router) # tämä tuo todo-reitittimen
app.include_router(admin.router) # tämä tuo admin-reitittimen
app.include_router(users.router) # tämä tuo käyttäjä-reitittimen