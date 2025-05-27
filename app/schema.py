from datetime import datetime
from importlib.resources import contents
from tarfile import PAX_NUMBER_FIELDS
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