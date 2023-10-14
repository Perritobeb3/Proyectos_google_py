#!/usr/bin/python3

import os
import requests
directorio = "supplier-data/descriptions/"
url = "http://localhost/upload/"

def lista_descripciones():
    im_list = []
    for file in os.listdir(directorio):
        if file != ".DS_Store":
            im_list.append(file)
    return im_list


def jsoncreate():
    fruits = []
    for file in lista_descripciones():
        with open(os.path.join(directorio, file), "r") as f:
            fread = f.readlines()
            x = {}
            x["name"] = fread[0].rstrip('\n')
            x["weight"] = int(fread[1].replace(" lbs",""))
            x["description"] = fread[2]
            x["image_name"] = "{file}.jpeg".format(file = file.replace(".txt",""))
            fruits.append(x)
    return fruits

def post(im):
    response = requests.post(url, json=im)

if __name__ == "__main__":
    post(jsoncreate())

        
            