#!/usr/bin/python3
#Necesitamos cambiar el formato, tamaño y orientación de una serie de imágenes.
#Primero importamos los módulos necesarios para ello: Pillow para las imágenes,
#Os para el sistema operativo y re para poder seleccionar los distintos archivos.
#También definimos dos directorios que nos servirán a la hora de interactuar con el OS.

import PIL
from PIL import Image
import os
import re
directorio = "/supplier-data/images"
directorio_out = "/supplier-data/images" 


#Tenemos que crear una lista con el nombre de todas las imágenes para poder luego editarlas automáticamente.
def lista_imagenes():
    #lee la carpeta donde están las imágenes para obtener una lista de todas las imágenes cuyo formato queremos cambiar.
    im_list = []
    formato_incorrecto = "\.tiff"
    for file in os.listdir(directorio):
        if file not in (".DS_Store","README","LICENSE"):
            im_list.append(file)
    return im_list

#necesitamos también una función que reescale, rote y cambie el formato de la imagen.
def transimagen(imagen_original):
    #esta función reescala, rota y cambia el formato de la imagen dada según los parámetros establecidos
    #guardando una copia con el mismo nombre en formato jpeg en el directorio deseado.
    angle_rot = 0
    filesize = (600,400)
    file_format = "jpeg"
    with Image.open(os.path.join(directorio, imagen_original)) as im:
        out = im.resize(filesize)
        out_rot = out.rotate(angle_rot)
        out_rot_RGB = out_rot.convert("RGB")
        out_rot_RGB.save(os.path.join(directorio_out, imagen_original), file_format)

#finalmente, montamos la función principal que se encargará de transformar cada imagen.
if __name__ == "__main__":
    #creamos la lista de imágenes para llevar a cabo el cambio:
    LM = lista_imagenes()
    #a cada imagen de esta lista le aplicamos la función de transformación.
    for image in LM:
        transimagen(image)
