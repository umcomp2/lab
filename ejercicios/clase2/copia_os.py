#!/usr/bin/python3
import os
archivo_origen=input("archivo origen: ")
archivo_destino=input("archivo destino: ")

fdo = os.open( archivo_origen, os.O_RDONLY )
fdd = os.open( archivo_destino, os.O_WRONLY | os.O_CREAT )
while True:
    leido = os.read(fdo, 102400)
    os.write(fdd, leido)
    print (str(len(leido)))
    if len(leido) != 1024:
        break

os.close(fdo)
os.close(fdd)
