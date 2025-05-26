from pickle import TRUE
from annotated_types import  Timezone
from sqlalchemy import TIMESTAMP, Column ,Integer, Nullable,String,Boolean, text ,false
from .database import Base

class Posts(Base):
    __tablename__='posts'
    
    id=Column(Integer,primary_key=True, nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='True',nullable=False)
    created_at=Column(TIMESTAMP(timezone=TRUE),nullable=false,server_default=text('now()'))
   

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True, nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=TRUE),nullable=false,server_default=text('now()'))
    

