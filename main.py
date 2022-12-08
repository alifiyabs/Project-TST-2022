from fastapi import FastAPI
from database.database import engine
from typing import List
#from passlib.context import CryptContext
from schemas import schemas
from models import models
from routers import users, parkiran

import uvicorn

app = FastAPI()

# Create table on database
models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(parkiran.router)


if __name__ == '__main__':
    uvicorn.run('main.app', host ='0.0.0.0', port=8000, reload=True)