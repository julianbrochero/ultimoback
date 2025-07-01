from pydantic import BaseModel, Field
from typing import Optional


class Categoria(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=5, max_length=30)
    descripcion: str = Field(min_length=5, max_length=100)
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Categoria 1",
                "descripcion": "Esta es la categoria 1"
            }
        }