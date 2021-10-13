#!/usr/bin/python3

import os 
import sys

os.chdir("/home/jlocamuz/3ro/compu2/lab/alumnos/59104-julia-locamuz/clase1")


try:
    if os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2]):
        print("existen los archivos")
        origen = open(sys.argv[1], 'r+')
        origen_contenido = origen.read()
        destino = open(sys.argv[2], 'w+')
        destino.write(origen_contenido)
        destino_contenido = destino.read()
        print(destino_contenido)
        origen.close()
        destino.close()
        print("copia realizada")
    else: 
        print("no existen los archivos")
except: 
    print("solo pasar dos archivos")
