from fastapi import FastAPI, Depends, status, Response
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List
import schemas
from models import models
import uvicorn

app = FastAPI()

# Create table on database
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create User and Add to database
@app.post('/user', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(email=request.email, username=request.username, password=request.password)

    db.add(new_user)
    db.commit()

    db.refresh(new_user)
    return new_user

# Create User and Add to database
@app.post('/motor', status_code=status.HTTP_201_CREATED)
def create_motor(request: schemas.Motor, db: Session = Depends(get_db)):
    new_motor = models.Motor(plat_motor=request.plat_motor)

    db.add(new_motor)
    db.commit()

    db.refresh(new_motor)
    return new_motor

# See the user that succesfully created (You can only see email and username)
@app.get('/user', response_model=List[schemas.UserView])
def get_user(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# See the user that succesfully created by id
@app.get('/user/{id}', status_code=200)
def get_user_by_id(id, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == id).first()
    return users

@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)

    db.commit()
    return {"Delete" : "Done!"}


if __name__ == '__main__':
    uvicorn.run('main.app', host ='0.0.0.0', port=8000, reload=True)
