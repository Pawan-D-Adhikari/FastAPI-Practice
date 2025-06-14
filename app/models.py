from sqlalchemy import TIMESTAMP, Column, ForeignKey ,Integer,String,Boolean, text

from app.routers import user 
from .database import Base
from sqlalchemy.orm import relationship 


class Posts(Base):
    __tablename__='posts'
    
    id=Column(Integer,primary_key=True, nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='True',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    owner=relationship("User")
   

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True, nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    verified=Column(Boolean,server_default=text('False'))  
    
class OTP(Base):
    __tablename__='otp'
    id=Column(Integer,primary_key=True, nullable=False)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    otp=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    expires_at=Column(TIMESTAMP(timezone=True),nullable=False)  # Add expiration time for OTP
    
class Vote(Base):
    __tablename__='votes'
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True,nullable=False)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True,nullable=False)
    
    

