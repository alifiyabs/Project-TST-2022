from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
import datetime
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    username = Column(String)
    password = Column(String)

class Motor(Base):
    __tablename__ = 'motor_mahasiswa'
    
    id = Column(Integer, primary_key=True, index=True)
    id_tempat_parkir = Column(Integer)
    plat_motor = Column(String)
    jam_masuk = Column(DateTime, default=datetime.datetime.utcnow)
    jam_keluar = Column(DateTime(timezone=True), onupdate=datetime.datetime.utcnow())

class TempatParkir(Base):
    __tablename__ = 'tempat_parkir_mahasiswa'

    id = Column(Integer, primary_key=True)
    tempat_parkir = Column(String)
    kuota = Column(Integer)