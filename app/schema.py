from datetime import datetime
from turtle import pos
from typing import Optional
from pydantic import BaseModel,EmailStr

from app.database import Base

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True
    
class PostCreate(PostBase):
    pass



class userResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime


class PostResponse(PostBase):
 
    id:int
    created_at:datetime
    owner:userResponse
    class Config:
     from_attributes=True
     
class PostOut(BaseModel):
    Post:PostResponse
    votes:int
    
    class Config:
     from_attributes=True
    

class userCreate(BaseModel):
    email:EmailStr
    password:str
    class Config:
        from_attributes=True
        
class userOtpverify(BaseModel):
    id:int
    otp:str
    
    class Config:
        from_attributes=True
    
class userLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int ] = None
    
    
class Vote(BaseModel):
    post_id:int
    dir:int
    
    class Config:
        from_attributes=True