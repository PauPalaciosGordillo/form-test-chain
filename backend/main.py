from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuarios/")
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre_completo,
        email=usuario.email,
        telefono=usuario.telefono,
        edad=usuario.edad,
        pais=usuario.pais,
        comentarios=usuario.comentarios
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {
        "id": nuevo_usuario.id,
        "nombre_completo": nuevo_usuario.nombre,  
        "email": nuevo_usuario.email,
        "telefono": nuevo_usuario.telefono,
        "edad": nuevo_usuario.edad,
        "pais": nuevo_usuario.pais,
        "comentarios": nuevo_usuario.comentarios
    }
