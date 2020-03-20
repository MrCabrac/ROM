import os.path as path
from os import listdir
from os import walk
import cv2
import numpy as np

class Log():
    def i(text):
        print("LOG:INFO -- ", text)
    
    def d(text):
        print("LOG:DEBUG -- ", text)
    
    def e(text):
        print("LOG:ERROR -- ", text)

def getConfigEntrenarPatch():
    try:
        with open("config.txt", encoding = "utf-8", mode = 'r') as f: #leer la carpeta de entrenar configurada
            text = f.readlines()
            print()
            if text[2].split("=")[0].strip() == 'entrenar_patch':
                entrenarPatch = text[2].split("=")[1].strip()
    except:
        entrenarPatch = 'entrenar'
        Log.e("La carpeta de 'entrenar' no fué encontrada")
    return entrenarPatch

class Config(object):
    def entrenarPatch():
        try:
            with open("config.txt", encoding = "utf-8", mode = 'r') as f: #leer la carpeta de entrenar configurada
                text = f.readlines()
                if text[2].split("=")[0].strip() == 'entrenar_patch':
                    entrenarPatch = text[2].split("=")[1].strip()
        except:
            entrenarPatch = 'entrenar'
            Log.e("La carpeta de 'entrenar' no fué encontrada")
        return entrenarPatch

    def saveModelPatch():
        try:
            with open("config.txt", encoding="utf-8", mode="r") as f:
                text = f.readlines()
                if text[3].split("=")[0].strip() == 'save_modelo_patch':
                    saveModelPatch = text[3].split("=")[1].strip()
        except:
            saveModelPatch = 'modelo'
        return saveModelPatch
    
    def frames():
        try:
            with open("config.txt", encoding = "utf-8", mode = 'r') as f: #leer la cantidad de frames configurada
                text = f.readlines()
                if text[1].split("=")[0].strip() == 'frames':
                    frames = int(text[1].split("=")[1].strip())
        except:
            frames = 30
        return frames

class Dimensionar(object):
    def __init__(self):
        self.entrenarPatch = getConfigEntrenarPatch()        

    def obtener_dimensiones(self):
        '''
        Obtener la dimension promedio de todas las imagenes usadas para el entrenamiento
        '''
        dimensiones_x = list() #guarda las dimensiones de todos los recortes en X
        dimensiones_y = list() #guarda las dimensiones de todos los recortes en Y
        en_x = 0
        en_y = 0
        for (path, ficheros, archivos) in walk(self.entrenarPatch):
            for imagen in archivos:
                img = cv2.imread(path+'/'+imagen, 0)
                [y, x] = img.shape
                dimensiones_x.append(x)
                dimensiones_y.append(y)
                en_x = int(np.mean(dimensiones_x))
                en_y = int(np.mean(dimensiones_y))

        del dimensiones_x, dimensiones_y
        return en_x, en_y

    def redimensionar(self, x, y):
        for (path, ficheros, archivos) in walk(self.entrenarPatch):
            for imagen in archivos:
                img = cv2.imread(path+'/'+imagen, 0)
                img = cv2.resize(img, (x, y))
                cv2.imwrite(path+'/'+imagen, img)
        return True