from config.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(128))  # Añadir el campo password
    rol = Column(String(50))

    reservas = relationship('Reserva', back_populates='usuario')
