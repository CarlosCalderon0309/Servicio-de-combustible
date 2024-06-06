import os
import hashlib
from typing import List
from fastapi import Form
from datetime import date
from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from .Conexion import SessionLocal, engine
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates  
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
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
            id_empleado=id_empleado
        )
        db.add(new_venta)
        db.commit()
        db.refresh(new_venta)
        return new_venta
    else:
        raise HTTPException(status_code=response.status_code, detail='Error al obtener los datos de la venta')