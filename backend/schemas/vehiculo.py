from pydantic import BaseModel, Field, EmailStr, field_validator, SecretStr
from fastapi import status
from typing import Optional, List
from fastapi.exceptions import HTTPException

class Vehiculo(BaseModel):
    id: Optional[int] = None
    marca: str = Field(min_length=5, max_length=30)
    modelo: str = Field(min_length=5, max_length=30)
    anio: int = Field(gt=0)
    matricula: str = Field(min_length=3, max_length=30)
    capacidad: int = Field(gt=0)
    categoria_id: int = Field(gt=0)
    
    
    class Config:
        json_scheme_extra = {
            "example": {
                "id": 1,
                "marca": "Toyota",
                "modelo": "Corolla",
                "anio": 2022,
                "matricula": "ABC123",
                "capacidad": 5,
                "categoria_id": 1
            }
        }