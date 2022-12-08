from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    email: str
    username: str
    password: str

class UserView(BaseModel):
    email: str
    username: str

    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Motor(BaseModel):
    plat_motor: str