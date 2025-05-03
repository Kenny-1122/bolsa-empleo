import pymysql
import pymysql.cursors
from db.db_mysql import get_db_connection
from models.administrador_model import Administrador
from fastapi.responses import JSONResponse

class AdministradorService:
    def __init__(self):
        self.con= get_db_connection()
        if self.con is None:
            print("No se pudo establecer conexión")
            
    #buscar 
    
    async def get_administradores(self):
        try:
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM  administrador")
                administrador=cursor.fetchall() #cuando hay varios registros en la BD
                
                
                return JSONResponse(
                    status_code=200,
                    content={
                        "succes": True, "message": "Administradores obtenidos exitosamente", "data": administrador if administrador else [] # si hay registros muestra, si no vacio
                    }
                )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                    content={
                        "succes": False, "message": f"Error al obtener los administradores {str}", "data": None
                    }
                )
        finally:    
            self.con.close() 
            
            
    #buscar por documento
    async def get_administrador_by_documento(self, documento_administrador: int):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM administrador WHERE documento_administrador = %s"
                cursor.execute(sql, (documento_administrador,))
                result = cursor.fetchone()
                if result:
                    return JSONResponse(
                        status_code=200,
                        content={"success": True, "message": "Administrador encontrado", "data": result}
                    )
                else:
                    return JSONResponse(
                        status_code=404,
                        content={"success": False, "message": "Administrador no encontrado", "data": None}
                    )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"Error: {str(e)}", "data": None}
            )
        finally:
            self.con.close()