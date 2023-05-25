Django Multitenant Store API

Este proyecto consiste en el backend utilizado para gestionar una multitienda basado en el principio multistore
requerimientos:
- pipenv
- redis
- postgresql
- wsl o linux.

Dado que el proyecto usa Django channels y redis, es recomendado ejecutarlo en linux, o en wsl si se tiene windows 10 en adelante.

Instrucciones de instalacion:<br>
`pipenv install`

antes de ejecutar el server hay que asegurarse de tener redis activo, para iniciar redis:<br>
`redis-server --port 6380`

Para Muchas partes del sistema es necesario ejecutar el worker de celery (no sin antes ejecutar redis):
`celery -A multistore worker`

Para activar el front del admin hay que instalar vue 2 en conjunto con sus dependencias:<br>

Ejecutar ese comando situandose en la carpeta vue-admin:
`npm install`


