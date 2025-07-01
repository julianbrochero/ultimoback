from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from backend.config.database import Session
from models.vehiculo import Vehiculo as VehiculoModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.vehiculo import VehiculoService
from schemas.vehiculo import Vehiculo
from utils.jwt_manager import create_token

vehiculo_router = APIRouter()

@vehiculo_router.get('/vehiculos', tags=['vehiculos'], response_model=List[Vehiculo], status_code=200)
def get_vehiculos() -> List[Vehiculo]:
    db = Session()
    result = VehiculoService(db).get_vehiculos()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@vehiculo_router.get('/vehiculos/{id}', tags=['vehiculos'], response_model=Vehiculo, dependencies=[Depends(JWTBearer())])
def get_vehiculo(id: int = Path(ge=1, le=2000)) -> Vehiculo:
    db = Session()
    result = VehiculoService(db).get_vehiculo(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Vehículo no encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@vehiculo_router.get('/vehiculos/marca/{marca}', tags=['vehiculos'], response_model=List[Vehiculo], dependencies=[Depends(JWTBearer())])
def get_vehiculo_by_marca(marca: str) -> List[Vehiculo]:
    db = Session()
    result = VehiculoService(db).get_vehiculo_by_marca(marca)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Vehículo no encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@vehiculo_router.get('/vehiculos/modelo/{modelo}', tags=['vehiculos'], response_model=List[Vehiculo], dependencies=[Depends(JWTBearer())])
def get_vehiculo_by_modelo(modelo: str) -> List[Vehiculo]:
    db = Session()
    result = VehiculoService(db).get_vehiculo_by_modelo(modelo)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Vehículo no encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@vehiculo_router.get('/vehiculos/categoria/{categoria_id}', tags=['vehiculos'], response_model=List[Vehiculo], dependencies=[Depends(JWTBearer())])
def get_vehiculo_by_categoria(categoria_id: int) -> List[Vehiculo]:
    db = Session()
    result = VehiculoService(db).get_vehiculo_by_categoria(categoria_id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Vehículo no encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@vehiculo_router.post('/vehiculos', tags=['vehiculos'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_vehiculo(vehiculo: Vehiculo) -> dict:
    db = Session()
    VehiculoService(db).create_vehiculo(vehiculo)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el vehiculo con éxito."})

@vehiculo_router.put('/vehiculos/{id}', tags=['vehiculos'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_vehiculo(id: int, vehiculo: Vehiculo)-> dict:
    db = Session()
    result = VehiculoService(db).get_vehiculo(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Vehiculo no encontrado"})
    
    VehiculoService(db).update_vehiculo(id, vehiculo)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado el vehiculo con éxito."})

@vehiculo_router.delete('/vehiculos/{id}', tags=['vehiculos'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_vehiculo(id: int)-> dict:
    db = Session()
    result: VehiculoModel = db.query(VehiculoModel).filter(VehiculoModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Vehículo no encontrado"})
    VehiculoService(db).delete_vehiculo(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado el vehiculo con éxito."})