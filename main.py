from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from routes.routes import routes, routes_b, routes_c, routes_d, routes_e, routes_f

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")


app= FastAPI()


app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")

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



 
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/empresa", response_class=HTMLResponse)
async def empresa(request: Request):
    return templates.TemplateResponse("index_empresa.html", {"request": request})



if __name__ =="__main__":
    uvicorn.run(app,host="0.0.0.0", port=8000, reload=True)