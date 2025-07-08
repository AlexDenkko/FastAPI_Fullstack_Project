from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Tämä määrittää tietokannan osoitteen.
#Tässä käytetään MySQL tietokantaa.
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:test123@127.0.0.1:3306/prompteddatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

