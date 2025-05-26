from ast import mod
from pyexpat import model
from turtle import pos
from fastapi import Depends, FastAPI 
from random import randrange
from  psycopg2.extras import RealDictCursor
import time
from .database import engine,get_db
from sqlalchemy.orm import Session
from .routers import post,user




app=FastAPI()


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
 return {"message":"Hello World"}





