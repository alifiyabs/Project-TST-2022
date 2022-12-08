from fastapi import APIRouter, HTTPException, status, Depends
from schemas import schemas
from typing import List
from models import models
from database import database
from datetime import datetime
from sqlalchemy.orm import Session

router = APIRouter()

# Create Motor parkir and Add to database
@router.post('/motor', status_code=status.HTTP_201_CREATED, tags=['Parkiran Motor'])
def create_motor_parkir(request: schemas.Motor, db: Session = Depends(database.get_db)):
    new_motor = models.Motor(plat_motor=request.plat_motor)

    db.add(new_motor)
    db.commit()

    db.refresh(new_motor)
    return new_motor


@router.patch('/motor/{plat_motor}', status_code=status.HTTP_202_ACCEPTED, tags=['Parkiran Motor'])
def motor_keluar(plat_motor, db: Session = Depends(database.get_db)):
    date_time = datetime.now
    db.query(models.Motor).filter(models.Motor.plat_motor == plat_motor).update({"jam keluar" : date_time})
    db.commit()
    return 'Motor sudah keluar!'

@router.get('/kepadatanparkiran', tags=['Parkiran Motor'])
def kepadatan_parkiran_harian(db: Session = Depends(database.get_db)):
    pass