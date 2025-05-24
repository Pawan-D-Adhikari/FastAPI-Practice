from ast import mod
from importlib.resources import contents
from turtle import pos, title
from fastapi import Depends, FastAPI ,Response, dependencies, status,HTTPException
from fastapi.params import Body
# from networkx import number_weakly_connected_components
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from  psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)



app=FastAPI()






class Post(BaseModel):
    title:str
    content:str
    published:bool=True
while True:
    try:
        conn=psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='pawan123',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database Connection was sucessful")
        break
    except Exception as error:
        print("Connecting to Db Failed")
        print("Error:",error)
        time.sleep(2)

    
my_posts=[{"title":'title of post 1','content':'content of post 1','id':1},{"title":'Fav food','content':'pizza','id':2}]



@app.get("/")
def root():
 return {"message":"Hello World"}



@app.get("/posts")
def get_posts(db: Session=Depends( get_db)):
   posts=db.query(models.Posts).all()
   return posts
  



@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post,db: Session=Depends(get_db) ):
    # new_post=models.Posts(title=post.title,content=post.content,published=post.published)
    new_post=models.Posts(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    
    



@app.get("/post/{id}")
def get_post(id:int,db: Session=Depends(get_db)): 
   

    post=db.query(models.Posts).filter(models.Posts.id==id).first()
   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} was not found")
    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM post WHERE id=%s RETURNING *""",(str(id),))
    # post=cursor.fetchone()
    # conn.commit()
    del_post=db.query(models.Posts).filter(models.Posts.id==id)
    if not del_post.one():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} was not found")
    del_post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)