from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

class UsuarioBase(BaseModel):
    nombre_completo: str
    email: EmailStr
    telefono: str
    edad: int = Field(..., gt=0, description="Debe ser mayor que 0")
    pais: str
    comentarios: Optional[str] = None

    @validator("telefono")
    def validar_telefono(cls, v):
        if not v.isdigit():
            raise ValueError("El teléfono solo debe contener dígitos")
        if not 7 <= len(v) <= 9:
            raise ValueError("El teléfono debe tener entre 7 y 9 dígitos")
        return v

class UsuarioCreate(UsuarioBase):
    pass
