from fastapi import Depends, status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from  .. import models,schema,utils
from ..database import get_db
from typing import List

router=APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.userResponse)
def create_user(user:schema.userCreate, db: Session=Depends(get_db)):
   
    hash_password=utils.hash(user.password )
    user.password=hash_password
    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 
    
    
@router.get("/{id}",response_model=schema.userResponse)
def get_user(id:int,db: Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exist")
    return user
    