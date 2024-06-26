from sqlalchemy.orm import Session
from app.models import User
from datetime import datetime
import bcrypt



def hash_otp(otp: str):
    salt = bcrypt.gensalt()
    hashed_otp = bcrypt.hashpw(str(otp).encode('utf-8'), salt)
    return hashed_otp

# def create_user(db: Session, email: str, password: str, name: str,phone_number:str):
#     db_user = User(email=email, password=password, name=name,phone_number=phone_number)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

def Check_user_email(db:Session,email:str):
    user=db.query(User).filter(User.email==email).first()
    return user

def update_otp(db: Session, OTP: str, email: str, expiry_time: datetime):
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.OTP = hash_otp(OTP)
        user.expires_at = expiry_time
        db.commit()
        db.refresh(user)
    return user

def update_refresh_token(db:Session,refresh_token:str,email:str):
   
   user=db.query(User).filter(User.email==email).first() 
   if user:
    user. refresh_token=refresh_token
    db.commit()
    db.refresh(user)
   else:
      print("no")
   return user

def Otp_check(db:Session,OTP:str):
   hashed_otp=hash_otp(OTP)
#    OTP=db.query(User).filter(User.OTP).first()
   user=db.query(User).filter(User.OTP==b'$2b$12$RbbdhxPvvQ6baCFdbESUIOf.CqHOG6iwmjx6Je1JiGdrErqSgAtti').first()
   print(user.email)
   return  user
