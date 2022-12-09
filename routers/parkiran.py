from fastapi import APIRouter, HTTPException, status, Depends
from schemas import schemas
from typing import List
from authentication import OAuth2
from models import models
from database import database
from datetime import datetime
from sqlalchemy.orm import Session

router = APIRouter(tags=["Parkiran Motor"])

# Create Motor parkir and Add to database
@router.post('/motor/{tempat_parkir}', status_code=status.HTTP_201_CREATED)
def create_motor_parkir(tempat_parkir: str, requset: schemas.Motor, db: Session = Depends(database.get_db)):

    ada_tempat_parkir = db.query(models.TempatParkir).filter(models.TempatParkir.tempat_parkir == tempat_parkir).first()
    if ada_tempat_parkir:
        new_motor = models.Motor(plat_motor = requset.plat_motor, id_tempat_parkir=ada_tempat_parkir.id)

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=["Tempat parkir tidak ditemukan!"])
    
    db.add(new_motor)

    db.commit()

    db.refresh(new_motor)
    return new_motor

@router.patch('/motor/{id}', status_code=status.HTTP_202_ACCEPTED)
def motor_keluar(id: int, db: Session = Depends(database.get_db)):
    ada_motor = db.query(models.Motor).filter(models.Motor.id == id).first()
    if ada_motor:
        n
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=["Motor tidak valid untuk keluar!"])
    db.add(new_keluar)

    db.commit()

    db.refresh(new_keluar)
    return new_keluar

@router.get('/kepadatanparkiran')
def kepadatan_parkiran_harian(db: Session = Depends(database.get_db)):
    pass