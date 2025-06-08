
from passlib.context import CryptContext
import random
from datetime import datetime, timedelta, timezone


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash(password: str):
     return pwd_context.hash(password)

def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def generate_otp():
    digits = [str(random.randint(0, 9)) for _ in range(6)]
    otp = ''.join(digits)
    return otp

def get_otp_expiry_time():
    
    return datetime.now(timezone.utc) + timedelta(minutes=5)  # OTP valid for 5 minutes

def get_current_time():
    return datetime.now(timezone.utc)  # Returns the current time in UTC