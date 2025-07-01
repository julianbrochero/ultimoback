from config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Vehiculo(Base):
    __tablename__ = 'vehiculo'
    id = Column(Integer, primary_key=True)
    marca = Column(String(50))
    modelo = Column(String(50))
    anio = Column(Integer)
    matricula = Column(String(50), unique=True)
    capacidad = Column(Integer)
    categoria_id = Column(Integer, ForeignKey('categoria.id'))

    categoria = relationship('Categoria', back_populates='vehiculos')
    reservas = relationship('Reserva', back_populates='vehiculo')
