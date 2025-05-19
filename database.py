from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DB_URL='postgrwsql://postgres:pawan123:localhost/fastapi'

engine=create_engine(SQLALCHEMY_DB_URL)

Sessionlocal=sessionmaker(autoflush=False,bind=engine)

Base=declarative_base()