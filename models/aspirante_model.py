from pydantic import BaseModel
from datetime import date

class Aspirante(BaseModel):
    documento_aspirante: int
    tipo_documento: str
    nombre: str
    fecha_nacimiento: date
    telefono: str
    correo_usuario: str  # Llave foránea con usuario
