#!/bin/bash

# Eliminar todos los contenedores en ejecución
docker rm -f $(docker ps -aq)

# Eliminar todas las imágenes
docker rmi -f $(docker images -aq)

# Eliminar todos los volúmenes no utilizados
docker volume prune -f
