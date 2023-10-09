#! /usr/bin/env python3

#para manejar los archivos de texto y 
#para enviar la opinion mediante Request, necesitamos varios modulos.

import requests
import os

dir_text = "/data/feedback"
url= "http://34.173.48.221/feedback/"

def text_to_dic(path):
    #devuelve el archivo de texto convertido en diccionario por lineas. 
    tipos = ("title", "name", "date", "feedback")
    datos = {}
    with open(path) as f:
        n = 0
        for line in f:
            datos[tipos[n]] = line.rstrip("\n")
            n = n+1
    return datos

#definimos la funcion que sera el loop que envie los archivos
def dic_to_post():
    for file in os.listdir(dir_text):
        dic = text_to_dic(os.path.join(dir_text,file))
        print(dic)
        response = requests.post(url, json=dic)
#esta ultima linea es solo necesaria si estamos debugeando un problema de conexion.
#        response.raise_for_status()

dic_to_post()