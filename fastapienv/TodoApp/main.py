from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
#Tämä luo tietokannan TODOAPP kansioon, jos se ei ole jo luotu.
#Tämä käyttää kaiken mitä database.py tiedostossa on määritelty sekä models.py tiedostossa.
#Tuo kaikki tapahtuu ja määriytyy SQLiten avulla, ei tarvitse itse kirjoittaa SQL komentoja.

app.include_router(auth.router)
app.include_router(todos.router)