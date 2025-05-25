import email
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
    class Config:
     orm_mode=True
    

class userCreate(BaseModel):
    email:EmailStr
    password:str