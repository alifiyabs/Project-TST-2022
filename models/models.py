from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    username = Column(String)
    password = Column(String)

# class Motor(Base):
#     __tablename__ = 'motor_mahasiswa'

#     id = Column(Integer, primary_key=True, index=True)
#     plat_motor = Column(String)
#     jam_masuk = Column(String(TIMESTAMP), nullable=False, server_default=func.now())