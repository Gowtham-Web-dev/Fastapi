from datetime import datetime, timedelta
from typing import Optional
from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal,get_db
from app.models import User
from .crud import Check_user_email,Otp_check
import bcrypt

SECRET_KEY = "55224-7723-#@!%"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_DAYS = 2

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def verify_password(plain_password, password):
    return pwd_context.verify(plain_password,password) # check the password

def get_password_hash(password):
    return pwd_context.hash(password) ## hash the password




def check_exist_user(db:Session,email:str,password:str):
    user=Check_user_email(db,email)
    if not user or not verify_password(password, user.password):
        return False
    return user


 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    encode_data = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(days=2)
    encode_data.update({"exp": expire})
    encoded_jwt = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def check_exist_user_eamil(db:Session,email:str):
    user=Check_user_email(db,email)
    return user


def Ckeck_OTP_valid(db:Session,OTP:str):
    user=Otp_check(db,OTP)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = Check_user_email(db, email)
    if user is None:
        raise credentials_exception
    return user