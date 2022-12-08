from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserView(BaseModel):
    email: str
    username: str

    class Config():
        orm_mode = True

class Login(BaseModel):
    username_using_email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Motor(BaseModel):
    plat_motor: str