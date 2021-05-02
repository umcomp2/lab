"""
2 - Escriba 3 programas similares. 
    Cada uno pide que se ingrese por teclado un nombre de archivo origen y luego uno destino. 
    Debe abrir ambos archivos, leer el primero y escribirlo en el segundo. 
    (use las funciones disponibles Built-in , en el modulo os, y en el modulo sys respectivamente)

./copia.py
archivo origen: prueba.txt
archivo destino: otro.txt

# diff prueba.txt otro.txt
#
"""

#!/usr/bin/python3

import os

origen = os.open("indicaciones_trabajo.txt", os.O_RDONLY)
destino = os.open("destino.txt", os.O_RDWR|os.O_CREAT)
while True:
    contenido= os.read(origen,1024)
    os.write(destino, contenido)
    if len(contenido) != 1024:
        break

os.close(origen)
os.close(destino)
