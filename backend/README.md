## Despliegue backend desarrollo
### Creacion de red para comunicacion entre contenedores 
```
docker network create --attachable connection_dockers
```
### Servicios bases de datos postgres con pgadmin
Ejecutar el siguiente comando para levantar los servicios de bd
en la carpeta databases
```
docker compose up -d
```
pgadmin esta en el localhost:8000

### CRUD 
Para ejecutar el contenedor de la api del CRUD se utilizando docker compose up en la carpeta CRUD
```
docker compose up -d
```
Utilizando solo el dockerfile

```
docker build -t crud -f Dockerfile.crud .  
```
```
docker run -v .:/app --name crud -p 4000:4000 --network connection_dockers crud
```
### API
Para ejecutar el contenedor de la API dentro de la carpeta se ejecuta solo
```
docker compose up -d
```
Utilizando solo el dockerfile

```
docker build -t api -f Dockerfile.api .  
```
```
docker run -v .:/app --name api -p 4000:4000 --network connection_dockers api
```