#!/usr/bin/python3
import os
archivo_origen = input("Ingrese el nombre del archivo origen: ")
archivo_destino = input("Ingrese el nombre del archivo destino: ")

def archivo_conjunto(archivo1, archivo2):
    if os.path.isfile(archivo1) and os.path.isfile(archivo2):
        archivo1 = open(archivo1,"r+")
        archivo2 = open(archivo2,"r+")
        archivo2.write(archivo1.read())
        archivo1.close()
        archivo2.close()
    else: 
        print("Hay un archivo que no existe rey")

variable = archivo_conjunto(archivo_origen,archivo_destino)
