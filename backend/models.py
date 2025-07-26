from sqlalchemy import Column, Integer, String
from backend.db import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    pais = Column(String, nullable=False)
    comentarios = Column(String, nullable=True)
