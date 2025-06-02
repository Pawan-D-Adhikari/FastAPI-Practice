from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import setting





SQLALCHEMY_DB_URL = f'postgresql://{setting.database_username}:{setting.database_password}@{setting.database_host}:{setting.database_port}/{setting.database_name}'




engine=create_engine(SQLALCHEMY_DB_URL)

Sessionlocal=sessionmaker(bind=engine,autoflush=False)

Base=declarative_base()

Base.metadata.create_all(bind=engine)

def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()