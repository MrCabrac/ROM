# ROM (Reconocimiento de operaciones matemáticas)
Permite analizar imágenes en busca de números y operadores matemáticos básicos usando OpenCV y ScikitLearn programado en Python. Puede identificar los números desde el 0 hasta el 9 y los operadores [-, +, *, /]

# Comenzando 🚀
Clonar el repositorio
```sh
git clone https://github.com/MrCabrac/ROM.git
```
## Pre-requisitos 📋
* [Python](https://www.python.org/downloads/)
* OpenCV
* Scikit learn
* Numpy

## Instalación 🔧
[Python](https://www.python.org/downloads/)

OpenCV
```
pip install opencv-python
```
Scikit learn
```sh
pip install -U scikit-learn
```

## Ejecutando las pruebas ⚙️
Para utilizar la cámara en vivo
```sh
py webcam.py "modelo/modeloEntrenado2.pkl"
```
Para entrenar a partir de un conjunto de imágenes:
```sh
py main.py train "modeloEntrenado2.pkl"
```
Para predecir de una imagen:
```sh
py predict "modelo/modeloEntrenado2.pkl" "imagenes de prueba/prueba.jpg"
```

## Construido con 🛠️
* Python
* OpenCV
* Scikit Learn SVC
* Numpy

## Contribuyendo 🖇️
...
## Wiki 📖
Revisar la [Wiki](https://github.com/MrCabrac/ROM/wiki)
## Versionado 📌
...
## Autores ✒️
* Brayan Martinez - Programación & Documentación - [MrCabrac](https://github.com/MrCabrac)

## Licencia 📄
...
## Expresiones de Gratitud 🎁
A Gustavo Moreno profesor de la Universidad EIA