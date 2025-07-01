from models.vehiculo import Vehiculo as VehiculoModel
from schemas.vehiculo import Vehiculo


class VehiculoService():
    
    def __init__(self, db) -> None:
        self.db = db

    def get_vehiculos(self):
        result = self.db.query(VehiculoModel).all()
        return result

    def get_vehiculo(self, id):
        result = self.db.query(VehiculoModel).filter(VehiculoModel.id == id).first()
        return result

    def get_vehiculo_by_marca(self, marca: str):
        result = self.db.query(VehiculoModel).filter(VehiculoModel.marca == marca).all()
        return result
    
    def get_vehiculo_by_modelo(self, modelo: str):
        result = self.db.query(VehiculoModel).filter(VehiculoModel.modelo == modelo).all()
        return result
    
    def get_vehiculo_by_categoria(self, categoria_id: int):
        result = self.db.query(VehiculoModel).filter(VehiculoModel.categoria_id == categoria_id).all()
        return result

    def create_vehiculo(self, vehiculo: Vehiculo):
        new_vehiculo = VehiculoModel(**vehiculo.model_dump())
        self.db.add(new_vehiculo)
        self.db.commit()
        return

    def update_vehiculo(self, id: int, data: Vehiculo):
        vehiculo = self.db.query(VehiculoModel).filter(VehiculoModel.id == id).first()
        vehiculo.marca = data.marca
        vehiculo.modelo = data.modelo
        vehiculo.anio = data.anio
        vehiculo.matricula = data.matricula
        vehiculo.capacidad = data.capacidad
        vehiculo.categoria_id = data.categoria_id
        self.db.commit()
        return

    def delete_vehiculo(self, id: int):
       self.db.query(VehiculoModel).filter(VehiculoModel.id == id).delete()
       self.db.commit()
       return