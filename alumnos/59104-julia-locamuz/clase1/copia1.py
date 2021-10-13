#!/usr/bin/python3

import os 

os.chdir("/home/jlocamuz/3ro/compu2/lab/alumnos/59104-julia-locamuz/clase1")

origen = input("archivo origen: ")
destino = input("archivo destino: ")

if os.path.isfile(origen) and os.path.isfile(destino):
    print("existen los archivos")
    origen = open(origen, 'r+')
    origen_contenido = origen.read()
    destino = open(destino, 'w+')
    destino.write(origen_contenido)
    destino_contenido = destino.read()
    print(destino_contenido)
    origen.close()
    destino.close()
else: 
    print("no existen los archivos")


