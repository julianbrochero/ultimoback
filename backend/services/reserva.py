from models.reserva import Reserva as ReservaModel
from schemas.reserva import Reserva
from sqlalchemy.orm import Session
from datetime import date

class ReservaService:
    
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_reservas(self):
        result = self.db.query(ReservaModel).all()
        return result

    def get_reserva(self, id: int):
        result = self.db.query(ReservaModel).filter(ReservaModel.id == id).first()
        return result

    def get_reserva_by_usuario(self, usuario_id: int):
        result = self.db.query(ReservaModel).filter(ReservaModel.usuario_id == usuario_id).all()
        return result
    
    def get_reserva_activa(self, usuario_id: int):
        now = date.now()
        result = self.db.query(ReservaModel).filter(ReservaModel.usuario_id == usuario_id, ReservaModel.fecha_devolucion >= now).all()
        return result

    def is_vehiculo_disponible(self, vehiculo_id: int, fecha_reserva: date, fecha_devolucion: date):
        existing_reservas = self.db.query(ReservaModel).filter(
            ReservaModel.vehiculo_id == vehiculo_id,
            ReservaModel.fecha_reserva < fecha_devolucion,
            ReservaModel.fecha_devolucion > fecha_reserva
        ).all()
        return len(existing_reservas) == 0

    def create_reserva(self, reserva: Reserva):
        if not self.is_vehiculo_disponible(reserva.vehiculo_id, reserva.fecha_reserva, reserva.fecha_devolucion):
            raise ValueError("El vehículo no está disponible para las fechas seleccionadas.")
        new_reserva = ReservaModel(**reserva.model_dump())
        self.db.add(new_reserva)
        self.db.commit()
        return new_reserva

    def update_reserva(self, id: int, data: Reserva):
        reserva = self.db.query(ReservaModel).filter(ReservaModel.id == id).first()
        if reserva:
            if not self.is_vehiculo_disponible(data.vehiculo_id, data.fecha_reserva, data.fecha_devolucion):
                raise ValueError("El vehículo no está disponible para las fechas seleccionadas.s")
            reserva.vehiculo_id = data.vehiculo_id
            reserva.usuario_id = data.usuario_id
            reserva.fecha_reserva = data.fecha_reserva
            reserva.fecha_devolucion = data.fecha_devolucion
            self.db.commit()
        return reserva

    def delete_reserva(self, id: int):
        self.db.query(ReservaModel).filter(ReservaModel.id == id).delete()
        self.db.commit()
        return
