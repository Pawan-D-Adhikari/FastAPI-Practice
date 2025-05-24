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
from . import schema
from sqlalchemy import false
from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)



app=FastAPI()











@app.get("/")
def root():
 return {"message":"Hello World"}



@app.get("/posts")
def get_posts(db: Session=Depends( get_db)):
   posts=db.query(models.Posts).all()
   return posts
  



@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:schema.Post,db: Session=Depends(get_db) ):

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
    del_post=db.query(models.Posts).filter(models.Posts.id==id)
    if not del_post.one():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} was not found")
    del_post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int,post: schema.Post,db: Session=Depends(get_db)):
    # post_query=db.query(models.Posts).filter(models.Posts.id==id)
    # db_post=post_query.first()
    # if not db_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # post_query.update(post.model_dump(),synchronize_session=False)
    # db.commit()
    # return {"data": post_query.first()}
    post_query=db.query(models.Posts).filter(models.Posts.id==id)
    post=post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}