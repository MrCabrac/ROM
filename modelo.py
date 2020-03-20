from os import walk
from os import path
from os import mkdir
import numpy as np
import cv2
import utilities
from sklearn.svm import SVC
import time
import joblib

class Modelo(object):
    def __init__(self):
        self.entrenarPatch = utilities.Config.entrenarPatch() #leer la carpeta donde estan las imagenes para entrenar
    
    def entrenar(self, fileName):
        imagenes = utilities.Dimensionar() #crear clase
        en_x, en_y = imagenes.obtener_dimensiones() #obtener el promedio de tamaño de todas las imagenes
        imagenes.redimensionar(en_x, en_y) #redimensionar todas las imagenes
        x = list() #lista para todas las imagenes
        y = list() #lista para la ruta de cada imagen que representa el codigo en ascii de cada caracter

        for (route, ficheros, archivos) in walk(self.entrenarPatch):
            for imagen in archivos:
                img = cv2.imread(route+'/'+imagen, 0)
                A = np.asarray(img).reshape(-1)
                x.append(A)
                y.append(route.split(chr(92))[1])
        numero_imagenes = 0
        categorias = 0
        for (route, ficheros, archivos) in walk(self.entrenarPatch):
            for carpeta in ficheros:
                categorias+=1
            for imagen in archivos:
                numero_imagenes+=1
        x = np.array(x)
        y = np.array(y)

        self.clf = SVC(probability=True, kernel='linear')
        utilities.Log.i("Numero de muestras {} en {} categorias.".format(numero_imagenes, categorias))
        utilities.Log.i("Tamaño de las imágenes: {} {} px.".format(en_x, en_y))
        utilities.Log.i("Entrenando...")
        timei = time.time()
        self.clf.fit(x, y)
        timef = time.time()
        utilities.Log.i("Ha tardado {} segundos.".format(timef-timei))
        '''Numero de imagenes en x categorias, tamaño de todas las imagenes y tiempo tardado'''
        info = [numero_imagenes, categorias, (en_x, en_y), timef-timei]
        del imagenes, en_x, en_y, x, y, numero_imagenes, categorias, timei, timef #borrar variables

        #Guardar el modelo en un archivo
        folder = utilities.Config.saveModelPatch()
        filePatch = folder + "/" + fileName
        if not path.isdir(folder): #si no existe la carpeta
            mkdir(folder)

        if path.exists(filePatch): #si el archivo existe, no lo vuelve a crear
            utilities.Log.i("El archivo ya existe, elimínelo, o ingrese otro nombre")
        else:
            joblib.dump(self.clf, filePatch) #crear archivo y guardar
            utilities.Log.i("El modelo fué guardado en '" + filePatch + "' | Size: " + str(path.getsize(filePatch)) + " bytes")

        del folder, filePatch
        return self.clf, info

