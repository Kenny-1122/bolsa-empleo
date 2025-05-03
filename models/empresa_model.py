from pydantic import BaseModel

class Empresa(BaseModel):
    nit: str
    nombre: str
    ciudad: str
    direccion: str
    correo: str  # Llave foránea con usuario
    telefono: str
