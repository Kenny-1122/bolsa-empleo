import pymysql
import pymysql.cursors
from db.db_mysql import get_db_connection
from models.oferta_model import Oferta
from fastapi.responses import JSONResponse

class OfertaService:
    def __init__(self):
        self.con= get_db_connection()
        if self.con is None:
            print("No se pudo establecer conexión")