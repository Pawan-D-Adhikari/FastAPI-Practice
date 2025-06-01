from fastapi import Depends,Response, status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from  .. import models,schema,oauth2
from ..database import get_db
from typing import List


router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schema.PostResponse])
def get_posts(db: Session=Depends( get_db),current_user: int = Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search: str = ""):
   posts=db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
   print(current_user.id)
   return posts

  



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.PostResponse)
def create_post(post:schema.PostCreate,db: Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    new_post=models.Posts(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    
    



@router.get("/{id}",response_model=schema.PostResponse,)
def get_single_post(id:int,db: Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)): 
   

    post=db.query(models.Posts).filter(models.Posts.id==id).first()
   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} was not found")
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    del_post=db.query(models.Posts).filter(models.Posts.id==id)

    
    if not del_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} was not found")
        
    if del_post.first().owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
  
    del_post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schema.PostResponse)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    existing_post = post_query.first()
    
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    
    if post_query.first().owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return  post_query.first()