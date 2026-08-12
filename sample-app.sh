#!/bin/bash

echo "Construyendo imagen Docker..."

docker build -t sampleapp .

echo "Deteniendo contenedor anterior..."

docker stop samplerunning 2>/dev/null
docker rm samplerunning 2>/dev/null

echo "Ejecutando contenedor..."

docker run -d \
--name samplerunning \
-p 5050:5050 \
sampleapp

echo "Contenedor iniciado correctamente"
