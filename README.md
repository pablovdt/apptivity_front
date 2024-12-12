# Apptivity Frontend Setup Guide

Este archivo proporciona las instrucciones necesarias para clonar y ejecutar el frontend de Apptivity en un servidor.
Este Front se conecta al backend de Apptivity (https://github.com/pablovdt/apptivity), necesario para su funcionamiento.
Es en el backend donde se crea la red y el contenedor apptivity que se usa en el Dockerfile de este repositorio.

## Clonar el Repositorio


```bash
git clone https://github.com/pablovdt/apptivity_front.git
```

### Accede al repositorio
```bash
cd apptivity
```

### Construye la imagen Docker
```bash
sudo docker build -t apptivity_front .
```

### Ejecuta el contenedor (La network es creada en el docker_compose.yml del backend)
```bash
sudo docker run -d --name apptivity_front --network apptivity_app_network -p 8501:8501 apptivity_front
```
#### Para detener el contenedor
```bash
sudo docker stop apptivity_front
```
### Para reiniciar el contenedor, utiliza:
```bash
sudo docker start apptivity_front
```
### Puedes verificar los logs del contenedor ejecutando:
```bash
sudo docker logs apptivity_front
```