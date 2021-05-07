#!/usr/bin/python3
import sys
#while True:
leido = sys.stdin.read()
sys.stderr.write("tamaño buffer " + str(len(leido)))
#parte en lineas
for renglon in leido.splitlines():
    #parte linea en palabras
    for palabra in renglon.split():
        #muestra al reves palabra[::-1] agrega espacio entre cada una
        sys.stdout.write(palabra[::-1]+" ")
    #agrega enter entre cada renglon
    sys.stdout.write("\n")    
    #valida que termino de leer el stdin   EOF 
    #if len(leido) != 1024:
    #    break
