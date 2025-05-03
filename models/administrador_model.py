from pydantic import BaseModel

class Administrador(BaseModel):
    documento_administrador: int
    tipo_documento: str
    nombre: str
    correo: str
    telefono: str
