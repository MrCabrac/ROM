# -*- coding: utf-8 -*-
"""
Creado en Fri Oct 19 05:19:22 2018

@autor: Steven's
"""

import cv2
from os import walk
import os

class Compare_images(object):
    def __init__(self, carpeta):
        self.__carpeta = carpeta

    def compare_images(self, imagen1, imagen2):
        img1 = cv2.imread(imagen1, 0)
        img2 = cv2.imread(imagen2, 0)
        try:
            img1.any()
            img2.any()
        except AttributeError:
            raise ValueError("Verifique la ruta de las imágenes.")
        result = (img1 == img2)
        if result.all():
            response = True
        else:
            response = False
        return response
    
    def delete_repeat_images(self, carpeta):
        rutas = list()
        for (path, ficheros, archivos) in walk(carpeta):
            for imagen in archivos:
                rutas.append(path+'/'+imagen)
        ##eliminar imagenes repetidas que sean totalmente identicas
        delete_list = list()
        for number in rutas:
            for second in rutas[rutas.index(number)+1:]:
                #print("{} - {}".format(number, second))
                result = self.compare_images(number, second)
        #        print(result)
                if result:
    #                print("Iguales: {} - {}".format(number, second))
                    #eliminar una de las 2
                    delete_list.append(number)
        delete_list = set(delete_list)
        for file in delete_list:
            print("Eliminar {}".format(file))
            os.remove(file)
        return delete_list

    def identical_images(self):
        carpetas = os.listdir(self.__carpeta)
        for carpeta in carpetas:
            path = self.__carpeta+'/'+carpeta
            self.delete_repeat_images(path)

comparar_imagenes = Compare_images('entrenar')
comparar_imagenes.identical_images()
