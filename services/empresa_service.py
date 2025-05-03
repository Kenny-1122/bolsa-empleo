import pymysql
import pymysql.cursors
from db.db_mysql import get_db_connection
from models.empresa_model import Empresa
from fastapi.responses import JSONResponse

class EmpresaService:
    def __init__(self):
        self.con = get_db_connection()
        if self.con is None:
            print("No se pudo establecer conexión")

    async def get_empresas(self):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT nit, nombre, ciudad, direccion, correo, telefono FROM empresa"
                cursor.execute(sql)
                empresas = cursor.fetchall()
            return JSONResponse(status_code=200, content={"success": True, "data": empresas})
        except Exception as e:
            return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

    async def get_empresa_by_nit(self, nit):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT nit, nombre, ciudad, direccion, correo, telefono FROM empresa WHERE nit=%s"
                cursor.execute(sql, (nit,))
                empresa = cursor.fetchone()
            if not empresa:
                return JSONResponse(status_code=404, content={"success": False, "detail": "Empresa no encontrada"})
            return JSONResponse(status_code=200, content={"success": True, "data": empresa})
        except Exception as e:
            return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

    async def create_empresa(self, data: Empresa):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                sql = """INSERT INTO empresa (nit, nombre, ciudad, direccion, correo, telefono)
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (data.nit, data.nombre, data.ciudad, data.direccion, data.correo, data.telefono))
            self.con.commit()
            return JSONResponse(status_code=201, content={"success": True, "message": "Empresa creada"})
        except Exception as e:
            return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

    async def update_empresa(self, nit, data: Empresa):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                sql = """UPDATE empresa SET nombre=%s, ciudad=%s, direccion=%s, correo=%s, telefono=%s
                         WHERE nit=%s"""
                cursor.execute(sql, (data.nombre, data.ciudad, data.direccion, data.correo, data.telefono, nit))
            self.con.commit()
            return JSONResponse(status_code=200, content={"success": True, "message": "Empresa actualizada"})
        except Exception as e:
            return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

    async def delete_empresa(self, nit):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                sql = "DELETE FROM empresa WHERE nit=%s"
                cursor.execute(sql, (nit,))
            self.con.commit()
            return JSONResponse(status_code=200, content={"success": True, "message": "Empresa eliminada"})
        except Exception as e:
            return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
