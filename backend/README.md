## Despliegue backend desarrollo
Ir a backend/databases y ejecutar el siguiente comando para levantar los servicios de bd
```
docker compose up -d
```
luego ejecutar desde la carpeta backend
```
python3 databases/createdatabases.py core
```