from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from backend.config.database import Session
from backend.models.usuario import Usuario as UsuarioModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.usuario import UsuarioService
from passlib.context import CryptContext
from utils.jwt_manager import create_token
from schemas.usuario import Usuario, UsuarioAuth
from fastapi.responses import JSONResponse

usuario_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(users:dict, email: str, password: str)->Usuario:
    user = get_user(users, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    user = Usuario.model_validate(user)
    return user

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user(users:list, email: str):
    for item in users:
        if item.email == email:
            return item

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)    

@usuario_router.post('/login', tags=['auth'])
def login(user: UsuarioAuth):
    db = Session()
    usuariosDb:UsuarioModel= UsuarioService(db).get_usuarios()
   
    usuario= authenticate_user(usuariosDb, user.email, user.password)
    if not user:
       return JSONResponse(status_code=401, content={'accesoOk': False,'token':''})  
    else:
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content={'accesoOk': True,'token':token, 'usuario': jsonable_encoder(usuario) })


@usuario_router.get('/usuarios', tags=['usuarios'], response_model=List[Usuario], status_code=200, dependencies=[Depends(JWTBearer())])
def get_usuarios() -> List[Usuario]:
    db = Session()
    result = UsuarioService(db).get_usuarios()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@usuario_router.get('/usuarios/{id}', tags=['usuarios'], response_model=Usuario, dependencies=[Depends(JWTBearer())])
def get_usuario(id: int = Path(ge=1, le=2000)) -> Usuario:
    db = Session()
    result = UsuarioService(db).get_usuario(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Usuario no encontrado."})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@usuario_router.get('/usuarios/', tags=['usuarios'], response_model=List[Usuario], dependencies=[Depends(JWTBearer())])
def get_usuario_by_email(email: str = Query(min_length=5, max_length=35)) -> List[Usuario]:
    db = Session()
    result = UsuarioService(db).get_usuario_by_email(email)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@usuario_router.post('/usuarios', tags=['usuarios'], response_model=dict, status_code=201)#, dependencies=[Depends(JWTBearer())])
def create_usuario(usuario: Usuario) -> dict:
    usuario.password = get_password_hash(usuario.password.get_secret_value())
    db = Session()
    UsuarioService(db).create_usuario(usuario)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el usuario con éxito."})


@usuario_router.put('/usuarios/{id}', tags=['usuarios'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_usuario(id: int, usuario: Usuario)-> dict:
    usuario.password = get_password_hash(usuario.password.get_secret_value())
    db = Session()
    result = UsuarioService(db).get_usuario(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Usuario no encontrado."})
    UsuarioService(db).update_usuario(id, usuario)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado el usuario con éxito."})


@usuario_router.delete('/usuarios/{id}', tags=['usuarios'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_usuario(id: int)-> dict:
    db = Session()
    result: UsuarioModel = db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontró el usuario."})
    UsuarioService(db).delete_usuario(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado el usuario con éxito."})