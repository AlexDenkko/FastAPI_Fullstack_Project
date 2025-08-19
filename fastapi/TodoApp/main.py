from fastapi import FastAPI, Request, status
from .models import Base # tämä tuo mallit, jotka määrittelevät tietokannan rakenteen
from .database import engine # tämä tuo moottorin tietokantayhteyttä varten
from .routers import auth, todos, admin, users # tämä tuo reitittimet eri toiminnallisuuksia varten
from fastapi.staticfiles import StaticFiles # tämä tuo staattiset tiedostot, kuten CSS ja JavaScript
from fastapi.responses import RedirectResponse #tämä tuo uudelleenohjausvastaukset

app = FastAPI() # alustaa FastAPI-sovelluksen

Base.metadata.create_all(bind=engine)
# Luo kaikki taulut tietokannassa, jotka on määritelty malleissa

app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static") # liittää staattiset tiedostot, kuten CSS ja JavaScript, TodoApp/static-hakemistosta


@app.get("/") 
def test(request: Request): 
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND) #tämä ohjaa käyttäjän todo-sivulle

@app.get("/healthy") # tämä on terveystarkistusreitti
def health_check():
    return {"status": "healthy"}
# tämä on terveystarkistus, joka palauttaa terveen tilan

app.include_router(auth.router) # tämä tuo autentikointireitittimen
app.include_router(todos.router) # tämä tuo todo-reitittimen
app.include_router(admin.router) # tämä tuo admin-reitittimen
app.include_router(users.router) # tämä tuo käyttäjä-reitittimen 