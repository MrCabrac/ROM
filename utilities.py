# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 22:27:15 2021

@author: Brayan.Martinez
"""

import os.path as path
from os import listdir
from os import walk
import cv2
import numpy as np

class Log():
    '''
        Recibe mensajes con diferente contexto para mostrar por consola
    '''
    def i(text):
        print("LOG:INFO -- ", text)
    
    def d(text):
        print("LOG:DEBUG -- ", text)
    
    def e(text):
        print("LOG:ERROR -- ", text)

class Config(object):
    def entrenarPatch():
        try:
            with open("config.txt", encoding = "utf-8", mode = 'r') as f: #leer la carpeta de entrenar configurada
                text = f.readlines()
                if text[2].split("=")[0].strip() == 'entrenar_patch':
                    entrenarPatch = text[2].split("=")[1].strip()
                    Log.d('Carpeta entrenar encontrada desde config.txt: "'+entrenarPatch+'"')
        except:
            entrenarPatch = 'entrenar'
            Log.e("La carpeta de 'entrenar' no fué encontrada, revise que config.txt está disponible")
        return entrenarPatch

    def saveModelPatch():
        try:
            with open("config.txt", encoding = "utf-8", mode="r") as f:
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
    
    def setModelSizes(x, y):
        try:
            with open("config.txt", encoding = "utf-8", mode = "r") as f:
                info = f.readlines()
                info[4] = "x_size = {}\n".format(x)
                info[5] = "y_size = {}\n".format(y)
            with open("config.txt", encoding = "utf-8", mode = "w") as f:
                f.writelines(info)
        except Exception as error:
            Log.e(error)
    
    def getModelSizes():
        try:
            with open("config.txt", encoding = "utf-8", mode = "r") as f:
                info = f.readlines()
                x = int(info[4].split("=")[1].strip())
                y = int(info[5].split("=")[1].strip())
        except Exception as error:
            Log.e(error)
            return False
        return x, y

class Dimensionar(object):
    def __init__(self):
        self.entrenarPatch = Config.entrenarPatch()        

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
        if en_x*en_y == 0:
            raise "No hay imágenes de entrenamiento X|{} Y|{}".format(en_x, en_y)
        else:
            Log.d("X|{} Y|{}".format(en_x, en_y))
        return en_x, en_y

    def redimensionar(self, x, y):
        for (path, ficheros, archivos) in walk(self.entrenarPatch):
            for imagen in archivos:
                img = cv2.imread(path+'/'+imagen, 0)
                img_y, img_x = img.shape
                if not (img_x == x) and (img_y == y):
                    img = cv2.resize(img, (x, y))
                    Log.d("Resizing img{}".format(imagen))
                    cv2.imwrite(path+'/'+imagen, img)
        return True

class Recortar(object):
    def __init__(self, ruta, margin, save, saved):
        self.margin = margin
        self.save = save
        self.saved = saved
        self.ruta = ruta
    
    def binarizar(self, thres1):
        ret1, thresh1 = cv2.threshold(thres1, 127, 255, cv2.THRESH_BINARY_INV) #binarizar
        del ret1
        return thresh1

    def contornos(self, img, contorno):
        cuadros = [] #una lista para guardar la coordenada de las esquinas de los cuadros
        for coordenada in contorno:
            xmenor = 10000
            xmayor = 0
            #------
            ymenor = 10000
            ymayor = 0
            x1, x2, y1, y2 = 0, 0, 0, 0
            for coordenada2 in coordenada:
                x = coordenada2[0][0]
                if x < xmenor:
                    xmenor = x
                elif x > xmayor:
                    xmayor = x
                y = coordenada2[0][1]
                if y < ymenor:
                    ymenor = y
                elif y > ymayor:
                    ymayor = y
                x1, x2, y1, y2 = xmenor, xmayor, ymenor, ymayor
            if x1 < 0:
                x1 = 0
            elif x2 < 0:
                x2 = 0
            elif y1 < 0:
                y1 = 0
            elif y2 < 0:
                y2 = 0
            cuadros.append([x1, x2, y1, y2]) # los [ ] eran (  )

        #Calcular el rectangulo más alto
        alturaMayor = 0
        for x1, x2, y1, y2 in cuadros:
            if (y2-y1) > alturaMayor:
                alturaMayor = y2-y1

        #Con el rectángulo más alto, normalizar los otros
        for cuadro in cuadros:
            if (cuadro[3]-cuadro[2]) < alturaMayor:
                pixelesFaltantes = (alturaMayor-(cuadro[3]-cuadro[2]))
                sumaPixeles = (pixelesFaltantes//2)
                cuadro[2]-=sumaPixeles
                cuadro[3]+=sumaPixeles+pixelesFaltantes%2
        #Marca los contornos para visualizarlos
# =============================================================================
#         copy_cuadros=cuadros
#         cuadros=list()
#         for x1,x2,y1,y2 in copy_cuadros:
#             cv2.rectangle(img,(x1-self.margin,y1-self.margin),(x2+self.margin,y2+self.margin),(0,255,255),15)
#             cuadros.append((x1,x2,y1,y2))
#         plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
#         plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
#         plt.show()
# =============================================================================
        return cuadros
    
    def recortes(self, img, cuadros, j): 
        '''
        Guardar cada recorte como una imagen a parte
        imagen de la cual se sacan recortes, coordenadas, margen de corte,variable de conteo
        '''
        imagenes = list() #lista para guardar los recortes generados
        for coordenada in cuadros:
            recorte = img[coordenada[2]-self.margin : coordenada[3]+self.margin, coordenada[0]-self.margin : coordenada[1]+self.margin] #obtener la imagen con las coordenadas + margin
            [fil, col] = recorte.shape #obtener las dimensiones del recorte
            if fil > 70: #si es lo suficientemente grande
                if col > 40: #si es lo suficientemente grande
                    imagenes.append(recorte) #agregar a la lista de recortes
            if (fil+1)/(col+1) < 2.3: #si poseen una propocion específica
                if self.save:
                    cv2.imwrite(self.saved+"/caracter{}.jpg".format(j), recorte)
            j+=1
        return j, imagenes

class main():
    def checkLog():
        Log.d("debug message")
        Log.e("error message")
        Log.i("information message")

    def checkConfig():
        Config.entrenarPatch()

    def CheckDimensionar():
        dim = Dimensionar()
        dim.obtener_dimensiones()

if __name__ == "__main__":
    print("Running utilities.py")
    # main.checkLog()
    # main.checkConfig()
    # main.CheckDimensionar()
else:
    print("Opening utilities.py")