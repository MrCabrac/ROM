import modelo

#Para entrenar solo se necesita una carpeta llamada 'entrenar' y dentro de esta la siguiente estructura
#
# entrenar
# | 40
#   | img1.jpg
#   | img2.jpg
#   | ...
# | 41
#   | img1.jpg
#   | ...
# ...
#
# El nombre de las carpetas que contienen las imagenes son el correspondiente desde ASCII al caracter que representan

#Para predecir necesita
#1. Hacer un modelo
#2. config.txt que siempre estará en el repositorio

modelClass = modelo.Modelo()

#To create a model
#modelClass.entrenar("modeloEntrenado.pkl")

#To predict
modelClass.predecir("modelo/modeloEntrenado.pkl", "imagenes de prueba/prueba.jpg")