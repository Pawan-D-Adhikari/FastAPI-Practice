from ast import mod
# from importlib.resources import contents
from traceback import print_list
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



@app.get("/posts",response_model=list[schema.PostResponse])
def get_posts(db: Session=Depends( get_db)):
   posts=db.query(models.Posts).all()
   return posts
  



@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schema.PostResponse)
def create_post(post:schema.PostCreate,db: Session=Depends(get_db) ):

    new_post=models.Posts(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    
    



@app.get("/post/{id}",response_model=schema.PostResponse)
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


from fastapi import HTTPException, status

@app.put("/posts/{id}",response_model=schema.PostResponse)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    existing_post = post_query.first()

    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return  post_query.first()


@app.post("/users",status_code=status.HTTP_201_CREATED)
def create_user(user:schema.userCreate, db: Session=Depends(get_db)):
    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    