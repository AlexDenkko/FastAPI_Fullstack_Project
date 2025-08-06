from fastapi import FastAPI, Request # tämä tuo FastAPI-sovelluskehyksen
from .models import Base # tämä tuo mallit, jotka määrittelevät tietokannan rakenteen
from .database import engine # tämä tuo moottorin tietokantayhteyttä varten
from .routers import auth, todos, admin, users # tämä tuo reitittimet eri toiminnallisuuksia varten
from fastapi.templating import Jinja2Templates # tämä tuo Jinja2-mallipohjat

app = FastAPI()

Base.metadata.create_all(bind=engine)
# Luo kaikki taulut tietokannassa, jotka on määritelty malleissa

templates = Jinja2Templates(directory="TodoApp/templates") # määrittelee mallipohjat hakemistosta


@app.get("/") # tämä on pääsivu, joka palauttaa tervetuloviestin
def test(request: Request): 
    return templates.TemplateResponse("home.html", {"request": request}) # palauttaa home.html-mallipohjan, joka sijaitsee TodoApp/templates-hakemistossa

@app.get("/healthy")
def health_check():
    return {"status": "healthy"}
# tämä on terveystarkistus, joka palauttaa terveen tilan

app.include_router(auth.router) # tämä tuo autentikointireitittimen
app.include_router(todos.router) # tämä tuo todo-reitittimen
app.include_router(admin.router) # tämä tuo admin-reitittimen
app.include_router(users.router) # tämä tuo käyttäjä-reitittimen