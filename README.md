# Servicio-de-combustible
Arquitectura de sistemas


Comandos para poder ejercutar el proyecto
antes que nada tener instalado lo siguiente para que funcione...

- pip install fastapi[all]
- pip install sqlalchemy
- pip install mysql
- pip install mysql-connector-python-rf
- pip install uvicorn 
- pip install mysql-connector-python (Comando para corregir los errores de conexion de la base de datos)

Crear una maquinaVirtual 
virtualenv env -p Python3 (Para crear la maquina virtual)

Teniendo descargado e instalado lo de arriba, se procede a ejecutar el siguiente comando para correr el proyecto

- uvicorn app.main:app --reload