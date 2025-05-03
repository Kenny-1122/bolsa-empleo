from pydantic import BaseModel

class Oferta(BaseModel):
    codigo_oferta: int
    descripcion: str
    nit: int  # Llave foránea con empresa
    estado_oferta: str
