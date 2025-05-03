from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from routes.routes import routes, routes_b, routes_c, routes_d, routes_e, routes_f


app= FastAPI()
app.title = "Proyecto CRUD"

#cargar archivo de variables de entorno
load_dotenv()

app.include_router(routes)
app.include_router(routes_b) #routes del bolsillo
app.include_router(routes_c)
app.include_router(routes_d)
app.include_router(routes_e)
app.include_router(routes_f)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"]
)

 
@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Default API",
    tags=["APP"]
)

def message():
    """Inicio del API
    
    
    Returns:
        Message
    """
    return HTMLResponse("<h1>Ejercicio de creación CRUD </h1>")

if __name__ =="__main__":
    uvicorn.run(app,host="0.0.0.0", port=8000, reload=True)