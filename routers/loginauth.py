from fastapi import APIRouter, Depends, HTTPException, status
from schemas import schemas
from models import models
from database import database
from authentication.hashing import HashPass
from authentication import jwt_tokens
from sqlalchemy.orm import Session

router = APIRouter(tags=['Login Authentication'])

@router.post('/login')
def user_login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username_using_email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kredensial yang dimasukkan salah!")

    if not HashPass.verify_password(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password yang dimasukkan salah!")
    
    access_token = jwt_tokens.create_access_token(
        data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
    return user

