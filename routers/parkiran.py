from fastapi import APIRouter, HTTPException, status, Depends
from schemas import schemas
from typing import List
from authentication import OAuth2
from models import models
from sqlalchemy import func
from database import database
from datetime import datetime
from sqlalchemy.orm import Session

router = APIRouter(tags=["Parkiran Motor"])

# Create Motor parkir and Add to database
# Motor yang masuk sesuai dengan tempat parkirnya dan tercatat jam masuknya.
@router.post('/motor/{tempat_parkir}', status_code=status.HTTP_201_CREATED,)
def create_motor_parkir(tempat_parkir: str, requset: schemas.Motor, db: Session = Depends(database.get_db),current_user: schemas.User = Depends(OAuth2.get_current_user)):

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
        ada_motor.update(jam_keluar=datetime.now())
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=["Motor tidak valid untuk keluar!"])
    db.commit()
    
    durasi = ada_motor.jam_keluar - ada_motor.jam_masuk
    durasi_detik = durasi.total_seconds()
    durasi_perjam = divmod(durasi_detik, 3600)[0]
    
    if (durasi_perjam <= 2):
        totalharga = 2000
    elif (durasi_perjam > 2):
        durasi_lebih = durasi_perjam - 2
        totalharga = 2000 + (1000*durasi_lebih)
    
    return {f'Harga yang harus dibayar adalah {totalharga} rupiah!'}

@router.get('/parkiran/sisa')
def sisa_slot(tempat_parkir: str, db: Session = Depends(database.get_db)):
    parkir = db.query(models.Motor.id_tempat_parkir, func.count(models.Motor.id).label('count')).group_by(models.Motor.id_tempat_parkir)
    park = db.query(models.TempatParkir).filter(models.TempatParkir.tempat_parkir == tempat_parkir.title()).first()
    if not park:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=["Nama parkiran tidak ditemukan"])
    for parkee in parkir:
        if (parkee["id_tempat_parkir"] == park.id):
            sisa_kuota = park.kuota - parkee["count"]
            return {"Sisa Kuota": f"{sisa_kuota} slot"}
    return (f'Kuota masih penuh yaitu {park.kuota} slot')
    

@router.get('/kepadatanparkiran')
def kepadatan_parkiran(tempat_parkir: str, db: Session = Depends(database.get_db)):
    parkir = db.query(models.Motor.id_tempat_parkir, func.count(models.Motor.id).label('count')).group_by(models.Motor.id_tempat_parkir)
    park = db.query(models.TempatParkir).filter(models.TempatParkir.tempat_parkir == tempat_parkir.title()).first()
    if not park:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=["Nama parkiran tidak ditemukan"])
    for parkee in parkir:
        if (parkee["id_tempat_parkir"] == park.id):
            kepadatan = (parkee["count"]/park.kuota)*100
            return {f"Kepadatan hari ini di parkiran {tempat_parkir.title()} adalah" : f"{kepadatan} %"}

@router.get('/kepadatanparkiran/{tempat_parkir}')
def kepadatan_parkiran_perwaktu(tempat_parkir: str, db: Session = Depends(database.get_db)):
    pass