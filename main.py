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

modelClass = modelo.Modelo()
modelClass.entrenar("modeloEntrenado.pkl")