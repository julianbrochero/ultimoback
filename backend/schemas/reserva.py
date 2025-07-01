from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Reserva(BaseModel):
    id: Optional[int] = None
    vehiculo_id: int = Field(gt=0)
    usuario_id: int = Field(gt=0)
    fecha_reserva: date
    fecha_devolucion: date

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "vehiculo_id": 1,
                "usuario_id": 1,
                "fecha_reserva": "2025-06-20",
                "fecha_devolucion": "2025-07-21"
            }
        }