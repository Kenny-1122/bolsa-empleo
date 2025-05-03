from pydantic import BaseModel

class AspiranteOferta(BaseModel):
    documento_aspirante: int  # FK con aspirante
    codigo_oferta: int        # FK con oferta
