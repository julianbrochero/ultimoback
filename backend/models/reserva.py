from config.database import Base
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

class Reserva(Base):
    __tablename__ = 'reserva'
    id = Column(Integer, primary_key=True)
    vehiculo_id = Column(Integer, ForeignKey('vehiculo.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    fecha_reserva = Column(Date)
    fecha_devolucion = Column(Date)

    # Relaciones con las tablas de vehículos y usuarios
    vehiculo = relationship('Vehiculo', back_populates='reservas')
    usuario = relationship('Usuario', back_populates='reservas')
