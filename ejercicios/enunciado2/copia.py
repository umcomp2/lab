#!/usr/bin/python3
import os

archivoOrigen = input("Ingrese el archivo origen: ")
archivoDestino = input("Ingrese el archivo destino: ")

def abrirArchivos(archivo1,archivo2):
    if os.path.isfile(archivo1) and os.path.isfile(archivo2):
        print("Los archivos existen")
        archivo3 = archivo1
        archivo3 = open(archivo3, "r+")
        archivo1 = open(archivo1, "r+")
        archivo2 = open(archivo2, "w+")
        print(archivo1.read())
        archivo2.write(archivo3.read())
        archivo2.close()
        archivo1.close()
        archivo3.close()
    else:
        print("Hay un archivo que no existe")



var = abrirArchivos(archivoOrigen, archivoDestino)
