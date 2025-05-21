from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DB_URL='postgresql://postgres:pawan123@localhost/fastapi'

engine=create_engine(SQLALCHEMY_DB_URL)

Sessionlocal=sessionmaker(bind=engine,autoflush=False)

Base=declarative_base()

def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()