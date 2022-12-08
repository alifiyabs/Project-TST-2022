from pydantic import BaseModel


class User(BaseModel):
    email: str
    username: str
    password: str

class UserView(BaseModel):
    email: str
    username: str

    class Config:
        orm_mode = True

class Motor(BaseModel):
    plat_motor: str