#!/usr/bin/env python3

import os
import time
from time import strftime, gmtime
from reports import generate
from emails import generate_mail, send

#generate the report text, para eso voy a reutilizar el script de run.py

texto_report = ""
directorio = "supplier-data/descriptions/"

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


def generate_report():
  report_name = "/tmp/processed.pdf"
  dic = jsoncreate()
  s = strftime("%a, %d %b %Y", 
               gmtime(time.time()))

  title = "Processed Update on {date}".format(date = s)
  texto_report = "<br/>"
  for item in dic:
      texto_report += "name: " + item["name"] +"<br/>"
      texto_report += "weight: " + str(item["weight"]) + " lbs" + "<br/><br/>"
  generate(report_name, title, texto_report)

sender = "automation@example.com"
recipient = "{}@example.com".format(os.environ.get('USER'))
subject = "Upload Completed - Online Fruit Store"
body = "All fruits are uploaded to our website successfully. A detailed list is attached to this email."
attachment_path = "/tmp/processed.pdf"

if __name__ == "__main__":
    generate_report()
    message = generate_mail(sender, recipient, subject, body, attachment_path)
    send(message)