from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from backend.config.database import engine, Base
from backend.middlewares.error_handler import ErrorHandler
from backend.routers.usuario import usuario_router
from backend.routers.vehiculo import vehiculo_router
from backend.routers.categoria import categoria_router
from backend.routers.reservas import reserva_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.title = "Sistema de Gestión de Alquiler de Vehículos"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

#Se defien los origenes que van a poder utitlizar oconsultar el backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(usuario_router)
app.include_router(vehiculo_router)
app.include_router(reserva_router)
app.include_router(categoria_router)


Base.metadata.create_all(bind=engine)


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')