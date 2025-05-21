from ast import mod
from fastapi import Depends, FastAPI ,Response, status,HTTPException
from fastapi.params import Body
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

def post_search(id):
    for p in my_posts:
        if p["id"]==id:
            return p
        
def post_search_index(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i

@app.get("/")
def root():
 return {"message":"Hello World"}

@app.get("/sqlalchemy")
def test_post(db: Session=Depends(get_db)):
    return{"Status":"Sucess"}


@app.get("/posts")
def get_posts():
   cursor.execute("""SELECT * FROM post """)
   posts=cursor.fetchall()
   return posts
  



@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute("""INSERT INTO post (title,content) VALUES (%s,%s) RETURNING * """,(post.title,post.content))
    new_post=cursor.fetchone()
    conn.commit()
    return new_post
    



@app.get("/post/{id}")
def get_post(id:int): 
   
    cursor.execute("""SELECT * FROM post WHERE id=%s""",(str(id)))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} was not found")
    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM post WHERE id=%s RETURNING *""",(str(id),))
    post=cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} was not found")
    
    return post
    
    
    
@app.put("/posts/{id}")
def update_post(id: int, payload: Post):
    cursor.execute("""UPDATE post SET title=%s,content=%s,published=%s WHERE id=%s returning *""",(payload.title,payload.content,payload.published,str(id)))
    post=cursor.fetchone()
    conn.commit()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    return post
    
    

    