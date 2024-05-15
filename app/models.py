from sqlalchemy import Column, Integer, String, DateTime, DATE, DECIMAL, ForeignKey
from .Conexion import Base

class Combustible(Base):
    __tablename__ = "Combustibles"
    id_combustible = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    tipo = Column(String(20))
    octanaje = Column(DECIMAL(4,2))
    
class Tanque(Base):
    __tablename__ = "Tanques"
    id_tanque = Column(Integer, primary_key=True, index=True)
    capacidad  = Column(DECIMAL(10,2))
    nivel_actual = Column(DECIMAL(10,2))
    id_combustible =  Column(Integer, ForeignKey('Combustibles.id_combustible'))
    
class Bomba(Base):
    __tablename__ = "Bombas"
    id_bomba = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer)
    estado = Column(String(20))
    id_tanque = Column(Integer, ForeignKey('Tanques.id_tanque'))
    
class Dispensador(Base):
    __tablename__ = "Dispensadores"
    id_dispensador = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer)
    id_bomba = Column(Integer, ForeignKey('Bombas.id_bomba'))
    
class Empleado(Base):
    __tablename__ = "Empleados"
    id_empleado = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    puesto = Column(String(20))
    
class Venta(Base):
    __tablename__ = "Ventas"
    id_venta = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime)
    cantidad = Column(DECIMAL(10,2))
    id_combustible = Column(Integer, ForeignKey('Combustibles.id_combustible'))
    id_dispensador = Column(Integer, ForeignKey('Dispensadores.id_dispensador'))
    id_empleado = Column(Integer, ForeignKey('Empleados.id_empleado'))
    
class Mantenimiento(Base):
    __tablename__ = "Mantenimientos"
    id_mantenimiento = Column(Integer, primary_key=True, index=True)
    fecha = Column(DATE)
    descripcion = Column(String(200))
    id_bomba = Column(Integer, ForeignKey('Bombas.id_bomba'))
    id_empleado = Column(Integer, ForeignKey('Empleados.id_empleado'))