from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True
    
class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
 
    id:int
    created_at:datetime
    owner_id:int
    class Config:
     from_attributes=True
    

class userCreate(BaseModel):
    email:EmailStr
    password:str
    
class userResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    
    
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
    