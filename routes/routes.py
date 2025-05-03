from fastapi import APIRouter

from models.administrador_model import Administrador
from models.aspirante_model import Aspirante
from models.aspirante_oferta_model import AspiranteOferta
from models.empresa_model import Empresa
from models.oferta_model import Oferta
from models.usuario_model import Usuario

from services.administrador_service import AdministradorService
from services.aspirante_service import AspiranteService
from services.aspirante_oferta_service import AspiranteOfertaService
from services.empresa_service import EmpresaService
from services.oferta_service import OfertaService
from services.usuario_service import UsuarioService

routes=APIRouter(prefix="/administrador", tags=["Administrador"])
routes_b=APIRouter(prefix="/aspirante", tags=["Aspirante"])
routes_c=APIRouter(prefix="/aspirante_oferta", tags=["AspiranteOferta"])
routes_d=APIRouter(prefix="/empresa", tags=["Empresa"])
routes_e=APIRouter(prefix="/oferta", tags=["Oferta"])
routes_f=APIRouter(prefix="/usuario", tags=["Usuario"])


administrador_service = AdministradorService()
aspirante_service = AspiranteService()
aspirante_oferta_service = AspiranteOfertaService()
empresa_service = EmpresaService()
oferta_service = OfertaService()
usuario_service = UsuarioService()

administrador_model=Administrador
aspirante_model=Aspirante
aspirante_oferta_model=AspiranteOferta
empresa_model=Empresa
oferta_model=Oferta
usuario_model=Usuario

#administrador
@routes.get("/get-administrador")
async def get_administrador():
        result= await administrador_service.get_administradores()
        return result

@routes.get("/get_administrador_by_documento/{documento_administrador}")
async def get_administrador_by_documento(documento_administrador: int):
    result = await administrador_service.get_administrador_by_documento(documento_administrador)
    return result

#aspirante

#aspirante oferta

#empresas

@routes_d.get("/get-empresa")
async def get_empresa():
    return await empresa_service.get_empresas()

@routes_d.get("/get-empresa/{nit}")
async def get_empresa(nit: int):
    return await empresa_service.get_empresa_by_nit(nit)

@routes_d.post("/create-empresa")
async def create_empresa(data: Empresa):
    return await empresa_service.create_empresa(data)

@routes_d.put("/update-empresa/{nit}")
async def update_empresa(nit: int, data: Empresa):
    return await empresa_service.update_empresa(nit, data)

@routes_d.delete("/delete-empresa/{nit}")
async def delete_empresa(nit: int):
    return await empresa_service.delete_empresa(nit)


#oferta

#usuario

@routes_f.get("/get-usuario")
async def get_users():
        result= await usuario_service.get_users()
        return result

@routes_f.post("/create-usuario")
async def create_usuario(data: Usuario):
    return await usuario_service.create_usuario(data)

@routes_f.get("/get-by-correo/{correo}")
async def get_usuario_by_correo(correo: str):
    result = await usuario_service.get_usuario_by_correo(correo)
    return result

@routes_f.patch("/change-password/")
async def change_password(correo: str, contrasena: str):
    return await usuario_service.change_password(correo, contrasena)



@routes_f.patch("/inactivate/{correo}")
async def inactivate_user(correo: str):
    return await usuario_service.inactivate_user(correo)

@routes_f.patch("/change-status/{correo}")
async def change_user_status(correo: str):
    return await usuario_service.toggle_user_status(correo)

@routes_f.put("/update-user/{correo}")
async def update_user(correo: str, user_data: Usuario):
    return await usuario_service.update_user(correo, user_data)

