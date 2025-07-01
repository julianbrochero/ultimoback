from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from backend.config.database import Session
from models.reserva import Reserva as ReservaModel
from schemas.reserva import Reserva
from services.reserva import ReservaService
from middlewares.jwt_bearer import JWTBearer
from fastapi.encoders import jsonable_encoder

reserva_router = APIRouter()

#Listar reservas
@reserva_router.get('/reservas', tags=['reservas'], response_model=List[Reserva], status_code=200, dependencies=[Depends(JWTBearer())])
def get_reservas() -> List[Reserva]:
    db = Session()
    result = ReservaService(db).get_reservas()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Obtener reserva por id
@reserva_router.get('/reservas/{id}', tags=['reservas'], response_model=Reserva, dependencies=[Depends(JWTBearer())])
def get_reserva(id: int = Path(..., ge=1, le=2000)) -> Reserva:
    db = Session()
    result = ReservaService(db).get_reserva(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Crear reserva
@reserva_router.post('/reservas', tags=['reservas'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_reserva(reserva: Reserva) -> dict:
    db = Session()
    try:
        ReservaService(db).create_reserva(reserva)
        return JSONResponse(status_code=201, content={"message": "Se ha registrado la reserva."})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Modificar reserva
@reserva_router.put('/reservas/{id}', tags=['reservas'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_reserva(id: int, reserva: Reserva) -> dict:
    db = Session()
    result = ReservaService(db).get_reserva(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    
    try:
        ReservaService(db).update_reserva(id, reserva)
        return JSONResponse(status_code=200, content={"message": "Se ha modificado la reserva."})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Eliminar reserva
@reserva_router.delete('/reservas/{id}', tags=['reservas'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_reserva(id: int) -> dict:
    db = Session()
    result: ReservaModel = db.query(ReservaModel).filter(ReservaModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontró"})
    ReservaService(db).delete_reserva(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la reserva."})


#Reservas activas de un usuario
@reserva_router.get('/reservas/activas/{usuario_id}', tags=['reservas'], response_model=List[Reserva], dependencies=[Depends(JWTBearer())])
def get_reserva_activa(usuario_id: int) -> List[Reserva]:
    db = Session()
    result = ReservaService(db).get_reserva_activa(usuario_id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No hay reservas activas para este usuario"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


#Obtener reservas por usuario
@reserva_router.get('/reservas/usuario/{usuario_id}', tags=['reservas'], response_model=List[Reserva], dependencies=[Depends(JWTBearer())])
def get_reserva_by_usuario(usuario_id: int) -> List[Reserva]:
    db = Session()
    result = ReservaService(db).get_reserva_by_usuario(usuario_id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Reservas no encontradas para este usuario"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

