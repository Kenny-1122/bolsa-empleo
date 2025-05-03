from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    correo: str
    contrasena: str
    estado: Optional[int] = 1  # Estado por defecto activo (1)