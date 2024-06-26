from fastapi import APIRouter,Depends,Body,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app import auth,crud,models,schemas,config
import jwt,hashlib
from jose import JWTError
from datetime import datetime, timedelta



router=APIRouter(
    prefix="/users",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

local_storage=[]

@router.post("/login")
async def login_token(form_data:schemas.User_Login, db: Session = Depends(get_db)):
    user = auth.check_exist_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = auth.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    refresh_token = auth.create_refresh_token(data={"sub": user.email}, expires_delta=refresh_token_expires)
    crud.update_refresh_token(db, refresh_token,user.email) #update the refresh_token to database
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/requestotp")
async def login_to_Otp(form_data:schemas.User_LoginBase, db: Session = Depends(get_db)):
    user = auth.check_exist_user_eamil(db, form_data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email")
    else:
       OTP=config.send_otp_email_for_login(user.email)
       expiry_time = datetime.utcnow() + timedelta(minutes=5)
       # hash and save the otp in database
       print(expiry_time)
       crud.update_otp(db,OTP,form_data.email,expiry_time)
       return()
      
@router.post("/verify_otp/")
async def verify_otp(otp:schemas.OTP,db:Session=Depends(get_db)):
   user = auth.Ckeck_OTP_valid(db,otp)
   print(user)
   return "ok"
   
@router.get("/users/me")
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return {"email": current_user.email, "full_name": current_user.name}


