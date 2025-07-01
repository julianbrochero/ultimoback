from pydantic import BaseModel, Field, EmailStr, field_validator, SecretStr, ConfigDict
from fastapi import status
from typing import Optional, List
from fastapi.exceptions import HTTPException
    
class UsuarioAuth(BaseModel):
    email: EmailStr
    password: str



class Usuario(BaseModel):
    id: Optional[int] = None
    nombre:str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: SecretStr = Field(min_length=8)
    rol: str = Field(default="2")
    
    model_config = ConfigDict(from_attributes=True)

    
