from pydantic import BaseModel,EmailStr,Field


class user(BaseModel):
      email:str
      password:str

class User_LoginBase(BaseModel):
      email:EmailStr
class User_Login(User_LoginBase):
      password:str=Field(...)

class OTP(BaseModel):
      Otp:str
