import os
from typing import List
from fastapi import Form
from datetime import date
from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
from .Conexion import SessionLocal, engine
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates  
from starlette.responses import RedirectResponse
import requests


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
current_directory = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(current_directory, "app", "plantillas"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get('/')
def inicio():
    return RedirectResponse(url='/docs/')

#peticiones para recibir todos los datos de la base de datos
@app.get('/mostar_datos_combustibles/', response_model=List[schemas.Datos_combustible])
def get_combustibles(db: Session = Depends(get_db)):
    combustibles = db.query(models.Combustible).all()
    return combustibles

@app.get('/mostar_datos_tanques/', response_model=List[schemas.Datos_tanque])
def get_tanques(db: Session = Depends(get_db)):
    tanques = db.query(models.Tanque).all()
    return tanques

@app.get('/mostar_datos_bombas/', response_model=List[schemas.Datos_bomba])
def get_bombas(db: Session = Depends(get_db)):
    bombas = db.query(models.Bomba).all()
    return bombas

@app.get('/mostar_datos_dispensadores/', response_model=List[schemas.Datos_dispensador])
def get_dispensadores(db: Session = Depends(get_db)):
    dispensadores = db.query(models.Dispensador).all()
    return dispensadores

@app.get('/mostar_datos_empleados/', response_model=List[schemas.Datos_empleado])
def get_empleados(db: Session = Depends(get_db)):
    empleados = db.query(models.Empleado).all()
    return empleados

@app.get('/mostar_datos_ventas/', response_model=List[schemas.Datos_venta])
def get_ventas(db: Session = Depends(get_db)):
    ventas = db.query(models.Venta).all()
    return ventas

@app.get('/mostar_datos_mantenimientos/', response_model=List[schemas.Datos_mantenimiento])
def get_mantenimientos(db: Session = Depends(get_db)):
    mantenimientos = db.query(models.Mantenimiento).all()
    return mantenimientos


#crer datos de nuestras tablas fuertes
@app.post('/crear_combustible/')
def crear_combustible(
    nombre: str = Form(...),
    tipo: str = Form(...),
    octanaje: float = Form(...),
    db: Session = Depends(get_db)
):
    new_combustible = models.Combustible(nombre=nombre, tipo=tipo, octanaje=octanaje)
    db.add(new_combustible)
    db.commit()
    db.refresh(new_combustible)
    return new_combustible

@app.post('/crear_tanque/')
def crear_tanque(
    capacidad: float = Form(...),
    nivel_actual: float = Form(...),
    id_combustible: int = Form(...),
    db: Session = Depends(get_db)
):
    new_tanque = models.Tanque(capacidad=capacidad, nivel_actual=nivel_actual, id_combustible=id_combustible)
    db.add(new_tanque)
    db.commit()
    db.refresh(new_tanque)
    return new_tanque

@app.post('/crear_bomba/')
def crear_bomba(
    numero: int = Form(...),
    estado: str = Form(...),
    id_tanque: int = Form(...),
    db: Session = Depends(get_db)
):
    new_bomba = models.Bomba(numero=numero, estado=estado, id_tanque=id_tanque)
    db.add(new_bomba)
    db.commit()
    db.refresh(new_bomba)
    return new_bomba

@app.post('/crear_dispensador/')
def crear_dispensador(
    numero: int = Form(...),
    id_bomba: int = Form(...),
    db: Session = Depends(get_db)
):
    new_dispensador = models.Dispensador(numero=numero, id_bomba=id_bomba)
    db.add(new_dispensador)
    db.commit()
    db.refresh(new_dispensador)
    return new_dispensador

#crear para mantenimiento
@app.post('/mantenimiento/')
def crear_mantenimiento(
    fecha: date = Form(...), #cambiar el atributo de int a date
    descripcion: str = Form(...),
    id_bomba: int = Form(...), 
    id_empleado: int = Form(...),
    db: Session = Depends(get_db)
):
    # Buscar la bomba en la base de datos
    bomba = db.query(models.Bomba).filter(models.Bomba.id_bomba == id_bomba).first()

    # Si la bomba no existe, retornar un error
    if not bomba:
        raise HTTPException(status_code=400, detail="Bomba no encontrada")

    # Buscar el empleado en la base de datos
    empleado = db.query(models.Empleado).filter(models.Empleado.id_empleado == id_empleado).first()

    # Si el empleado no existe, retornar un error
    if not empleado:
        raise HTTPException(status_code=400, detail="Empleado no encontrado")

    # Si la bomba y el empleado existen, crear el nuevo mantenimiento
    new_mantenimiento = models.Mantenimiento(fecha=fecha, descripcion=descripcion, id_bomba=id_bomba, id_empleado=id_empleado)
    db.add(new_mantenimiento)
    db.commit()
    db.refresh(new_mantenimiento)
    return new_mantenimiento



#recibir datos de otras apis
@app.post('/crear_empleado/')
def crear_empleado(
    db: Session = Depends(get_db)
):
    # Hacer una solicitud a la API externa para obtener los datos del empleado
    response = requests.get('http://localhost:5002/empleados')  #cambiar cuando nos den la verdadera api
    if response.status_code == 200:
        empleado_data = response.json()
        # Crear el objeto de empleado en la base de datos
        new_empleado = models.Empleado(nombre=empleado_data['nombre'], apellido=empleado_data['apellido'], puesto=empleado_data['puesto'])
        db.add(new_empleado)
        db.commit()
        db.refresh(new_empleado)
        return new_empleado
    else:
        raise HTTPException(status_code=response.status_code, detail='Error al obtener los datos del empleado')
    
@app.post('/crear_venta/')
def recibir_pago(
    id_combustible: int = Form(...),
    id_dispensador: int =  Form(...),
    id_empleado: int = Form(...),
    db: Session = Depends(get_db)
):
    # Hacer una solicitud a la API externa para obtener los datos de la venta
    response = requests.get('http://localhost:5002/ventas')
    if response.status_code == 200:
        venta_data = response.json()
        # Crear el objeto de venta en la base de datos
        new_venta = models.Venta(
            fecha=venta_data['fecha'], 
            cantidad=venta_data['cantidad'], 
            id_combustible=id_combustible, 
            id_dispensador=id_dispensador, 
            id_empleado=id_empleado,
        )
        db.add(new_venta)
        db.commit()
        db.refresh(new_venta)
        return new_venta
    else:
        raise HTTPException(status_code=response.status_code, detail='Error al obtener los datos de la venta')
    
#actualizar datos
@app.put('/actualizar_combustible/{id_combustible}')
def actualizar_combustible(
    id_combustible: int,
    nombre: str = Form(None),
    tipo: str = Form(None),
    octanaje: float = Form(None),
    db: Session = Depends(get_db)
):
    combustible = db.query(models.Combustible).filter(models.Combustible.id_combustible == id_combustible).first()
    if not combustible:
        raise HTTPException(status_code=404, detail="Combustible no encontrado")
    if nombre:
        combustible.nombre = nombre
    if tipo:
        combustible.tipo = tipo
    if octanaje:
        combustible.octanaje = octanaje
    db.commit()
    db.refresh(combustible)
    return combustible

@app.put('/actualizar_tanque/{id_tanque}')
def actualizar_tanque(
    id_tanque: int,
    capacidad: float = Form(None),
    nivel_actual: float = Form(None),
    id_combustible: int = Form(None),
    db: Session = Depends(get_db)
):
    tanque = db.query(models.Tanque).filter(models.Tanque.id_tanque == id_tanque).first()
    if not tanque:
        raise HTTPException(status_code=404, detail="Tanque no encontrado")
    if capacidad:
        tanque.capacidad = capacidad
    if nivel_actual:
        tanque.nivel_actual = nivel_actual
    if id_combustible:
        tanque.id_combustible = id_combustible
    db.commit()
    db.refresh(tanque)
    return tanque

@app.put('/actualizar_bomba/{id_bomba}')
def actualizar_bomba(
    id_bomba: int,
    numero: int = Form(None),
    estado: str = Form(None),
    id_tanque: int = Form(None),
    db: Session = Depends(get_db)
):
    bomba = db.query(models.Bomba).filter(models.Bomba.id_bomba == id_bomba).first()
    if not bomba:
        raise HTTPException(status_code=404, detail="Bomba no encontrada")
    if numero:
        bomba.numero = numero
    if estado:
        bomba.estado = estado
    if id_tanque:
        bomba.id_tanque = id_tanque
    db.commit()
    db.refresh(bomba)
    return bomba

@app.put('/actualizar_dispensador/{id_dispensador}')
def actualizar_dispensador(
    id_dispensador: int,
    numero: int = Form(None),
    id_bomba: int = Form(None),
    db: Session = Depends(get_db)
):
    dispensador = db.query(models.Dispensador).filter(models.Dispensador.id_dispensador == id_dispensador).first()
    if not dispensador:
        raise HTTPException(status_code=404, detail="Dispensador no encontrado")
    if numero:
        dispensador.numero = numero
    if id_bomba:
        dispensador.id_bomba = id_bomba
    db.commit()
    db.refresh(dispensador)
    return dispensador

@app.put('/actualizar_empleado/{id_empleado}')
def actualizar_empleado(
    id_empleado: int,
    nombre: str = Form(None),
    apellido: str = Form(None),
    puesto: str = Form(None),
    db: Session = Depends(get_db)
):
    empleado = db.query(models.Empleado).filter(models.Empleado.id_empleado == id_empleado).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    if nombre:
        empleado.nombre = nombre
    if apellido:
        empleado.apellido = apellido
    if puesto:
        empleado.puesto = puesto
    db.commit()
    db.refresh(empleado)
    return empleado

@app.put('/actualizar_venta/{id_venta}')
def actualizar_venta(
    id_venta: int,
    fecha: date = Form(None),
    cantidad: float = Form(None),
    id_combustible: int = Form(None),
    id_dispensador: int = Form(None),
    id_empleado: int = Form(None),
    db: Session = Depends(get_db)
):
    venta = db.query(models.Venta).filter(models.Venta.id_venta == id_venta).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    if fecha:
        venta.fecha = fecha
    if cantidad:
        venta.cantidad = cantidad
    if id_combustible:
        venta.id_combustible = id_combustible
    if id_dispensador:
        venta.id_dispensador = id_dispensador
    if id_empleado:
        venta.id_empleado = id_empleado
    db.commit()
    db.refresh(venta)
    return venta

@app.put('/actualizar_mantenimiento/{id_mantenimiento}')
def actualizar_mantenimiento(
    id_mantenimiento: int,
    fecha: date = Form(None),
    descripcion: str = Form(None),
    id_bomba: int = Form(None),
    id_empleado: int = Form(None),
    db: Session = Depends(get_db)
):
    mantenimiento = db.query(models.Mantenimiento).filter(models.Mantenimiento.id_mantenimiento == id_mantenimiento).first()
    if not mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    if fecha:
        mantenimiento.fecha = fecha
    if descripcion:
        mantenimiento.descripcion = descripcion
    if id_bomba:
        mantenimiento.id_bomba = id_bomba
    if id_empleado:
        mantenimiento.id_empleado = id_empleado
    db.commit()
    db.refresh(mantenimiento)
    return mantenimiento

#eliminar datos
@app.delete('/eliminar_combustible/{id_combustible}')
def eliminar_combustible(id_combustible: int, db: Session = Depends(get_db)):
    combustible = db.query(models.Combustible).filter(models.Combustible.id_combustible == id_combustible).first()
    if not combustible:
        raise HTTPException(status_code=404, detail="Combustible no encontrado")
    db.delete(combustible)
    db.commit()
    return combustible

@app.delete('/eliminar_tanque/{id_tanque}')
def eliminar_tanque(id_tanque: int, db: Session = Depends(get_db)):
    tanque = db.query(models.Tanque).filter(models.Tanque.id_tanque == id_tanque).first()
    if not tanque:
        raise HTTPException(status_code=404, detail="Tanque no encontrado")
    db.delete(tanque)
    db.commit()
    return tanque

@app.delete('/eliminar_bomba/{id_bomba}')
def eliminar_bomba(id_bomba: int, db: Session = Depends(get_db)):
    bomba = db.query(models.Bomba).filter(models.Bomba.id_bomba == id_bomba).first()
    if not bomba:
        raise HTTPException(status_code=404, detail="Bomba no encontrada")
    db.delete(bomba)
    db.commit()
    return bomba

@app.delete('/eliminar_dispensador/{id_dispensador}')
def eliminar_dispensador(id_dispensador: int, db: Session = Depends(get_db)):
    dispensador = db.query(models.Dispensador).filter(models.Dispensador.id_dispensador == id_dispensador).first()
    if not dispensador:
        raise HTTPException(status_code=404, detail="Dispensador no encontrado")
    db.delete(dispensador)
    db.commit()
    return dispensador

@app.delete('/eliminar_empleado/{id_empleado}')
def eliminar_empleado(id_empleado: int, db: Session = Depends(get_db)):
    empleado = db.query(models.Empleado).filter(models.Empleado.id_empleado == id_empleado).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    db.delete(empleado)
    db.commit()
    return empleado

@app.delete('/eliminar_venta/{id_venta}')
def eliminar_venta(id_venta: int, db: Session = Depends(get_db)):
    venta = db.query(models.Venta).filter(models.Venta.id_venta == id_venta).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    db.delete(venta)
    db.commit()
    return venta

@app.delete('/eliminar_mantenimiento/{id_mantenimiento}')
def eliminar_mantenimiento(id_mantenimiento: int, db: Session = Depends(get_db)):
    mantenimiento = db.query(models.Mantenimiento).filter(models.Mantenimiento.id_mantenimiento == id_mantenimiento).first()
    if not mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    db.delete(mantenimiento)
    db.commit()
    return mantenimiento

#peticiones para recibir un solo dato de la base de datos
@app.get('/mostrar_combustible/{id_combustible}', response_model=schemas.Datos_combustible)
def get_combustible(id_combustible: int, db: Session = Depends(get_db)):
    combustible = db.query(models.Combustible).filter(models.Combustible.id_combustible == id_combustible).first()
    if not combustible:
        raise HTTPException(status_code=404, detail="Combustible no encontrado")
    return combustible

@app.get('/mostrar_tanque/{id_tanque}', response_model=schemas.Datos_tanque)
def get_tanque(id_tanque: int, db: Session = Depends(get_db)):
    tanque = db.query(models.Tanque).filter(models.Tanque.id_tanque == id_tanque).first()
    if not tanque:
        raise HTTPException(status_code=404, detail="Tanque no encontrado")
    return tanque

@app.get('/mostrar_bomba/{id_bomba}', response_model=schemas.Datos_bomba)
def get_bomba(id_bomba: int, db: Session = Depends(get_db)):
    bomba = db.query(models.Bomba).filter(models.Bomba.id_bomba == id_bomba).first()
    if not bomba:
        raise HTTPException(status_code=404, detail="Bomba no encontrada")
    return bomba

@app.get('/mostrar_dispensador/{id_dispensador}', response_model=schemas.Datos_dispensador)
def get_dispensador(id_dispensador: int, db: Session = Depends(get_db)):
    dispensador = db.query(models.Dispensador).filter(models.Dispensador.id_dispensador == id_dispensador).first()
    if not dispensador:
        raise HTTPException(status_code=404, detail="Dispensador no encontrado")
    return dispensador

@app.get('/mostrar_empleado/{id_empleado}', response_model=schemas.Datos_empleado)
def get_empleado(id_empleado: int, db: Session = Depends(get_db)):
    empleado = db.query(models.Empleado).filter(models.Empleado.id_empleado == id_empleado).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado

@app.get('/mostrar_venta/{id_venta}', response_model=schemas.Datos_venta)
def get_venta(id_venta: int, db: Session = Depends(get_db)):
    venta = db.query(models.Venta).filter(models.Venta.id_venta == id_venta).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

@app.get('/mostrar_mantenimiento/{id_mantenimiento}', response_model=schemas.Datos_mantenimiento)
def get_mantenimiento(id_mantenimiento: int, db: Session = Depends(get_db)):
    mantenimiento = db.query(models.Mantenimiento).filter(models.Mantenimiento.id_mantenimiento == id_mantenimiento).first()
    if not mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    return mantenimiento

#peticiones para recibir datos de la base de datos por nombre
# @app.get('/buscar_combustible/{nombre}', response_model=List[schemas.Datos_combustible])
# def buscar_combustible(nombre: str, db: Session = Depends(get_db)):
#     combustible = db.query(models.Combustible).filter(models.Combustible.nombre == nombre).all()
#     if not combustible:
#         raise HTTPException(status_code=404, detail="Combustible no encontrado")
#     return combustible

# @app.get('/buscar_tanque/{capacidad}', response_model=List[schemas.Datos_tanque])
# def buscar_tanque(capacidad: float, db: Session = Depends(get_db)):
#     tanque = db.query(models.Tanque).filter(models.Tanque.capacidad == capacidad).all()
#     if not tanque:
#         raise HTTPException(status_code=404, detail="Tanque no encontrado")
#     return tanque

# @app.get('/buscar_bomba/{numero}', response_model=List[schemas.Datos_bomba])
# def buscar_bomba(numero: int, db: Session = Depends(get_db)):
#     bomba = db.query(models.Bomba).filter(models.Bomba.numero == numero).all()
#     if not bomba:
#         raise HTTPException(status_code=404, detail="Bomba no encontrada")
#     return bomba

# @app.get('/buscar_dispensador/{numero}', response_model=List[schemas.Datos_dispensador])
# def buscar_dispensador(numero: int, db: Session = Depends(get_db)):
#     dispensador = db.query(models.Dispensador).filter(models.Dispensador.numero == numero).all()
#     if not dispensador:
#         raise HTTPException(status_code=404, detail="Dispensador no encontrado")
#     return dispensador

# @app.get('/buscar_empleado/{nombre}', response_model=List[schemas.Datos_empleado])
# def buscar_empleado(nombre: str, db: Session = Depends(get_db)):
#     empleado = db.query(models.Empleado).filter(models.Empleado.nombre == nombre).all()
#     if not empleado:
#         raise HTTPException(status_code=404, detail="Empleado no encontrado")
#     return empleado

# @app.get('/buscar_venta/{fecha}', response_model=List[schemas.Datos_venta])
# def buscar_venta(fecha: date, db: Session = Depends(get_db)):
#     venta = db.query(models.Venta).filter(models.Venta.fecha == fecha).all()
#     if not venta:
#         raise HTTPException(status_code=404, detail="Venta no encontrada")
#     return venta

# @app.get('/buscar_mantenimiento/{fecha}', response_model=List[schemas.Datos_mantenimiento])
# def buscar_mantenimiento(fecha: date, db: Session = Depends(get_db)):
#     mantenimiento = db.query(models.Mantenimiento).filter(models.Mantenimiento.fecha == fecha).all()
#     if not mantenimiento:
#         raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
#     return mantenimiento
