import modelo
import sys
try:
    firstCommand = sys.argv[1]
except IndexError as error:
    firstCommand = ""

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

# Help
if(firstCommand == ""):
    print("train 'modeloEntrenado.pkl'")
    print("predict 'modelo/modeloEntrenado.pkl' 'imagenes de prueba/prueba.jpg'")

#To create a model
if(firstCommand == "train"):
    '''
    secondCommand must be like "modeloEntrenado.pkl"
    '''
    modelClass = modelo.Modelo()
    secondCommand = sys.argv[2]
    modelClass.entrenar(secondCommand)

#To predict
if(firstCommand == "predict"):
    '''
    secondCommand is a trained model and must be like "modelo/modeloEntrenado.pkl"
    thirdCommand is an image and must be like "imagenes de prueba/prueba.jpg"
    '''
    modelClass = modelo.Modelo()
    secondCommand = sys.argv[2]
    thirdCommand = sys.argv[3]
    modelClass.predecir(secondCommand, thirdCommand)