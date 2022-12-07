from fastapi import FastAPI, Depends
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List
import schemas
from models import models
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(email=request.email, username=request.username, password=request.password)

    db.add(new_user)
    db.commit()

    db.refresh(new_user)
    return new_user

@app.get('/user', response_model=List[schemas.UserView])
def get_user(db: Session = Depends(get_db)):
    return db.query(models.User).all()

if __name__ == '__main__':
    uvicorn.run('main.app', host ='0.0.0.0', port=8000, reload=True)
