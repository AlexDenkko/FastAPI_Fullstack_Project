from sqlalchemy import create_engine # tämä luo tietokantamoottorin
from sqlalchemy.orm import sessionmaker, declarative_base # tämä luo session, jota käytetään tietokannan kanssa
from sqlalchemy.ext.declarative import declarative_base # tämä luo perusluokan, jota käytetään ORM-mallien kanssa

#Tämä määrittää tietokannan osoitteen.
#Tässä käytetään MySQL tietokantaa.
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:test123@127.0.0.1:3306/prompteddatabase'
#Tässä määritellään SQLAlchemy tietokannan moottori.

engine = create_engine(SQLALCHEMY_DATABASE_URL) 
#Tämä luo tietokantamoottorin SQLAlchemy:lle.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Tämä luo session, jota käytetään tietokannan kanssa.

Base = declarative_base()
#Tämä luo perusluokan, jota käytetään ORM-mallien kanssa.

