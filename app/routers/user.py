from fastapi import Depends, status,HTTPException,APIRouter
from pydantic import EmailStr
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
    otp=send_otp(new_user.id, db)  # Automatically send OTP after user creation
    print(otp)
    return new_user 

# @router.get("/sendotp/{id}", status_code=status.HTTP_200_OK)
def send_otp( id: int ,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exist")
    otp = utils.generate_otp()
    if not otp:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to generate OTP")
    expiry_time= utils.get_otp_expiry_time()
    new_otp = models.OTP(user_id=id, otp=otp, expires_at=expiry_time)
    db.add(new_otp)
    db.commit()
    otp=db.query(models.OTP).filter(models.OTP.user_id == id).first()
    return otp.otp




@router.post("/verifyotp", status_code=status.HTTP_200_OK)
def verify_otp(user_otp:schema.userOtpverify, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_otp.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {user_otp.id} does not exist")
    
    otp_record = db.query(models.OTP).filter(models.OTP.user_id == user_otp.id,models.OTP.otp==user_otp.otp).first()
    if not otp_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid OTP")
    
    if otp_record.expires_at < utils.get_current_time():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="OTP has expired")
    
    user.verified = True
    db.commit()
    return {"message": "OTP verified successfully"}
    
    
    
    
    
    
    
@router.get("/{id}",response_model=schema.userResponse)
def get_user(id:int,db: Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exist")
    return user
    