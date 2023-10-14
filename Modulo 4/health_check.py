#!/usr/bin/env python3

#this file should work with a crontab or something similar

import shutil
import psutil
import socket
from emails import generate_mail, send

#Revisamos si sucede alguna de las condiciones problematicas.
def check_issues():
    mail_line = ""
    if psutil.cpu_percent(1) > 80:
        mail_line += "Error - CPU usage is over 80%"
    if psutil.disk_usage("/")[3] > 80:
        mail_line += "Error - Available disk space is less than 20%"
    if (psutil.virtual_memory()[1]/1048576) < 500:
        mail_line += "Error - Available memory is less than 500MB"
    if socket.gethostbyname('localhost') != '127.0.0.1':
        mail_line += "Error - localhost cannot be resolved to 127.0.0.1"
    return mail_line

if __name__ == "__main__":
    mail_line = check_issues()
    sender = "automation@example.com"
    recipient = "{}@example.com".format(os.environ.get('USER'))
    body = "Please check your system and resolve the issue as soon as possible."
    if mail_line != "":
        message = generate_mail(sender, recipient, mail_line, body)
        send(message)



