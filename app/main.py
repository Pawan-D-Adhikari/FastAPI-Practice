from ast import mod
from fastapi import  FastAPI 
from random import randrange
from  psycopg2.extras import RealDictCursor
import time
from .database import engine,get_db
from .routers import post,user,auth




app=FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
 return {"message":"Hello World"}





