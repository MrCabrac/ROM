# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 22:27:15 2021

@author: Brayan.Martinez
"""

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
        '''
        fileName: Model filename to save it like fileName.pkl
        '''
        imagenes = utilities.Dimensionar() #crear clase
        try:
            en_x, en_y = imagenes.obtener_dimensiones() #obtener el promedio de tamaño de todas las imagenes
            utilities.Config.setModelSizes(en_x, en_y)
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

        except TypeError as error:
            utilities.Log.e(error)
        except FileNotFoundError as error:
            utilities.Log.e(error)

    def predecir(self, clf_patch, image_patch):
        #TODO: revisar si todos los archivos existen
        self.clf = joblib.load(clf_patch) #cargar un modelo ya entrenado
        texto = str()
        img = cv2.imread(image_patch, 0) #leer la imagen a identificar
        ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV) #binarizar
        contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #obtener todos los contornos
        caracteres = utilities.Recortar(image_patch, 10, True, "caracteres") #crear clase
        cuadros = caracteres.contornos(thresh1, contours) #se obtienen todos los cuadros identificados
        cuadros.sort() #ordenar los cuadros, esto hace que se lea de izquierda a derecha
        j = 0 #Contador de imagenes
        j, imganalizar = caracteres.recortes(thresh1, cuadros, j) #obtener la lista con los recortes de imagen
        dimensiones = utilities.Dimensionar() #crear clase
        en_x, en_y = dimensiones.obtener_dimensiones()
        #TODO: Verificar que las imagenes de entrenamiento sigan en promedio con esos tamaños y leer los tamaños del config
        xSize, ySize = utilities.Config.getModelSizes() #obtener dimensiones desde los datos que guarda el modelo
        utilities.Log.i("Dimensiones de imagen: X|{} Y|{}".format(xSize, ySize))
        if not (en_x==xSize and en_y==ySize):
            utilities.Log.d("Hay imágenes nuevas en 'entrenar', vuelva a realizar el modelo.")
        utilities.Log.i("Comenzando a analizar")
        for imagen in imganalizar:
            imagen = cv2.resize(imagen, (xSize, ySize)) #redimensiona la imagen al mismo tamaño con las cuales se entreno el modelo
            B = np.asarray(imagen).reshape(-1) #convertir imagen a array
            response = self.clf.predict([B]) #prediccion
            texto = texto+str(chr(int(response[0]))) #sumar texto
        utilities.Log.i("Resultado: " + texto)
        del ret, hierarchy, xSize, ySize, en_x, en_y #eliminar variables
        
        return texto, thresh1

    def fPredecir(self, image_patch):
        pass
        #TODO: mirar si así se mejora el rendimiento, sin necesidad de cargar el (modelo, config) x veces