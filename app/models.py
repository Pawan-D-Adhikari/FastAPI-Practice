from pickle import TRUE
from annotated_types import  Timezone
from sqlalchemy import TIMESTAMP, Column, ForeignKey ,Integer, Nullable,String,Boolean, text 
from .database import Base

class Posts(Base):
    __tablename__='posts'
    
    id=Column(Integer,primary_key=True, nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='True',nullable=False)
    created_at=Column(TIMESTAMP(timezone=TRUE),nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
   

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True, nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=TRUE),nullable=False,server_default=text('now()'))
    

