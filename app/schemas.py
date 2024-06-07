from pydantic import BaseModel
from typing import Optional


#mostrar los datos que se encunetran el a base de datos
class Datos_combustible(BaseModel):
    id_combustible: Optional[int]
    nombre: Optional[str]
    tipo: Optional[str]
    octanaje: Optional[float]
    
    class Config: 
        from_attributes = True
        
class Datos_tanque(BaseModel):
    id_tanque: Optional[int]
    capacidad: Optional[float]
    nivel_actual: Optional[float]
    id_combustible: Optional[int]
    
    class Config: 
        from_attributes = True
        
class Datos_bomba(BaseModel):
    id_bomba: Optional[int]
    numero: Optional[int]
    estado: Optional[str]
    id_tanque: Optional[int]
    
    class Config: 
        from_attributes = True
        
class Datos_dispensador(BaseModel):
    id_dispensador: Optional[int]
    numero: Optional[int]
    id_bomba: Optional[int]
    
    class Config: 
        from_attributes = True
        
class Datos_empleado(BaseModel):
    id_empleado: Optional[int]
    nombre: Optional[str]
    apellido: Optional[str]
    puesto: Optional[str]
    
    class Config: 
        from_attributes = True
        
class Datos_venta(BaseModel):
    id_venta: Optional[int]
    fecha: Optional[str]
    cantidad: Optional[float]
    id_combustible: Optional[int]
    id_dispensador: Optional[int]
    id_empleado: Optional[int]
    
    class Config: 
        from_attributes = True
        
class Datos_mantenimiento(BaseModel):
    id_mantenimiento: Optional[int]
    fecha: Optional[str]
    descripcion: Optional[str]
    id_bomba: Optional[int]
    id_empleado: Optional[int]
    
    class Config: 
        from_attributes = True

#crear los datos que se van a insertar en la base de datos
class crear_combustible(BaseModel):
    nombre: str
    tipo: str
    octanaje: float
    
    class Config:
        from_attributes = True
    
class crear_tanque(BaseModel):
    capacidad: float
    nivel_actual: float
    id_combustible: int
    
    class Config:
        from_attributes = True
    
class crear_bomba(BaseModel):
    numero: int
    estado: str
    id_tanque: int
    
    class Config:
        from_attributes = True
    
class crear_dispensador(BaseModel):
    numero: int
    id_bomba: int
    
    class Config:
        from_attributes = True
    
class crear_empleado(BaseModel):
    nombre: str
    apellido: str
    puesto: str
    
    class Config:
        from_attributes = True
    
class crear_venta(BaseModel):
    fecha: str
    cantidad: float
    id_combustible: int
    id_dispensador: int
    id_empleado: int
    
    class Config:
        from_attributes = True
    
class crear_mantenimiento(BaseModel):
    fecha: str
    descripcion: str
    id_bomba: int
    id_empleado: int
    
    class Config:
        from_attributes = True


#mostrar los datos sin el optional
class Datos_combustible1(BaseModel):
    id_combustible: int
    nombre: str
    tipo: str
    octanaje: float
    
    class Config: 
        from_attributes = True

class Datos_tanque1(BaseModel):
    id_tanque: int
    capacidad: float
    nivel_actual: float
    id_combustible: int
    
    class Config: 
        from_attributes = True

class Datos_bomba1(BaseModel):
    id_bomba: int
    numero: int
    estado: str
    id_tanque: int
    
    class Config: 
        from_attributes = True

class Datos_dispensador1(BaseModel):
    id_dispensador: int
    numero: int
    id_bomba: int
    
    class Config: 
        from_attributes = True

class Datos_empleado1(BaseModel):
    id_empleado: int
    nombre: str
    apellido: str
    puesto: str
    
    class Config: 
        from_attributes = True

class Datos_venta1(BaseModel):

    id_venta: int
    fecha: str
    cantidad: float
    id_combustible: int
    id_dispensador: int
    id_empleado: int
    
    class Config: 
        from_attributes = True

class Datos_mantenimiento1(BaseModel):

    id_mantenimiento: int
    fecha: str
    descripcion: str
    id_bomba: int
    id_empleado: int
    
    class Config: 
        from_attributes = True


