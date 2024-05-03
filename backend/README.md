## Despliegue backend desarrollo
Ejecutar el siguiente comando para levantar los servicios de bd
en la carpeta databases
```
docker compose up -d
```
pgadmin esta en el localhost:8000
Para ejecutar el contenedor de la api del CRUD se utilizando docker compose up en la carpeta CRUD
```
docker compose up -d
```
Utilizando solo el dockerfile
```
docker build -t crud -f Dockerfile.crud .  
```
```
docker run -v .:/app --name crud -p 4000:4000 crud 
```