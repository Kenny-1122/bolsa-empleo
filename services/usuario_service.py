import pymysql
import pymysql.cursors
from db.db_mysql import get_db_connection
from models.usuario_model import Usuario
from fastapi.responses import JSONResponse

class UsuarioService:
    def __init__(self):
        self.con= get_db_connection()
        if self.con is None:
            print("No se pudo establecer conexión")
    
    #buscar usuarios
    
    async def get_users(self):
        try:
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM  usuario")
                users=cursor.fetchall() #cuando hay varios registros en la BD
                
                
                return JSONResponse(
                    status_code=200,
                    content={
                        "succes": True, "message": "Usuarios obtenidos exitosamente", "data": users if users else [] # si hay registros muestra, si no vacio
                    }
                )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                    content={
                        "succes": False, "message": f"Error al obtener los usuarios {str}", "data": None
                    }
                )
  
    
    #crear usuarios

    async def create_usuario(self, data: Usuario):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                sql = """INSERT INTO usuario (correo, contrasena)
                         VALUES (%s, %s)"""
                cursor.execute(sql, (
                    data.correo,
                    data.contrasena
                ))
                self.con.commit()
                return JSONResponse(
                    status_code=200,
                    content={"success": True, "message": "Usuario creado exitosamente", "data": {"correo": cursor.lastrowid}}
                )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"No se pudo crear el usuario: {str(e)}", "data": None}
            )

             
    #buscar usuario por correo
    async def get_usuario_by_correo(self, correo: str):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM usuario WHERE correo = %s"
                cursor.execute(sql, (correo,))
                result = cursor.fetchone()
                if result:
                    return JSONResponse(
                        status_code=200,
                        content={"success": True, "message": "Usuario encontrado", "data": result}
                    )
                else:
                    return JSONResponse(
                        status_code=404,
                        content={"success": False, "message": "Usuario no encontrado", "data": None}
                    )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": f"Error al obtener el usuario: {str(e)}", "data": None}
            )

            
    #cambiar contraseña
    
    async def change_password(self, correo: str, contrasena: str):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                check_sql = "SELECT COUNT(*) FROM usuario WHERE correo=%s"
                cursor.execute(check_sql, (correo,))
                result = cursor.fetchone()
                
                if result[0] == 0:
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                sql = "UPDATE usuario SET contrasena=%s WHERE correo=%s"
                cursor.execute(sql, (contrasena, correo))
                self.con.commit()

                if cursor.rowcount > 0:
                    return JSONResponse(content={"success": True, "message": "Contraseña actualizada exitosamente."}, status_code=200)
                else:
                    return JSONResponse(content={"success": False, "message": "No se realizaron cambios."}, status_code=409)
        except Exception as e:
            self.con.rollback()
            return JSONResponse(content={"success": False, "message": f"Error al actualizar la contraseña: {str(e)}"}, status_code=500)


    async def inactivate_user(self, correo: str):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                check_sql = "SELECT COUNT(*) FROM usuario WHERE correo=%s"
                cursor.execute(check_sql, (correo,))
                result = cursor.fetchone()
                
                if result[0] == 0:
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                sql = "UPDATE usuario SET estado=0 WHERE correo=%s"
                cursor.execute(sql, (correo,))
                self.con.commit()

                if cursor.rowcount > 0:
                    return JSONResponse(content={"success": True, "message": "Usuario inactivado exitosamente."}, status_code=200)
                else:
                    return JSONResponse(content={"success": False, "message": "No se realizaron cambios."}, status_code=400)
        except Exception as e:
            self.con.rollback()
            return JSONResponse(content={"success": False, "message": f"Error al inactivar usuario: {str(e)}"}, status_code=500)


    async def toggle_user_status(self, correo: str):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                get_estado_sql = "SELECT estado FROM usuario WHERE correo=%s"
                cursor.execute(get_estado_sql, (correo,))
                result = cursor.fetchone()

                if not result:
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                estado_actual = result[0]
                nuevo_estado = 0 if estado_actual == 1 else 1

                update_sql = "UPDATE usuario SET estado=%s WHERE correo=%s"
                cursor.execute(update_sql, (nuevo_estado, correo))
                self.con.commit()

                return JSONResponse(content={"success": True, "message": "Estado actualizado correctamente."}, status_code=200)
        except Exception as e:
            self.con.rollback()
            return JSONResponse(content={"success": False, "message": f"Error al cambiar estado: {str(e)}"}, status_code=500)

    async def update_user(self, correo: str, user_data):
        try:
            self.con.ping(reconnect=True)
            with self.con.cursor() as cursor:
                check_sql = "SELECT COUNT(*) FROM usuario WHERE correo=%s"
                cursor.execute(check_sql, (correo,))
                result = cursor.fetchone()

                if result[0] == 0:
                    return JSONResponse(content={"success": False, "message": "Usuario no encontrado."}, status_code=404)

                update_sql = """
                    UPDATE usuario
                    SET correo=%s, contrasena=%s
                    WHERE correo=%s
                """
                cursor.execute(update_sql, (
                    user_data.correo,
                    user_data.contrasena,
                    correo
                ))
                self.con.commit()

                if cursor.rowcount > 0:
                    return JSONResponse(content={"success": True, "message": "Usuario actualizado correctamente."}, status_code=200)
                else:
                    return JSONResponse(content={"success": False, "message": "No se realizaron cambios."}, status_code=409)

        except Exception as e:
            self.con.rollback()
            return JSONResponse(content={"success": False, "message": f"Error al actualizar usuario: {str(e)}"}, status_code=500)
