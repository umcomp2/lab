import os
import argparse
import multiprocessing as mp
import cabecera
from argumentos import validar_argumentos

analizador = argparse.ArgumentParser()
analizador.add_argument("-s", "--size", help="Bloque de bytes que se van a leer")
analizador.add_argument("-f", "--file", help="Archivo en formato ppm")
analizador.add_argument("-g", help="Escala para verde")
analizador.add_argument("-r", help="Escala para rojo")
analizador.add_argument("-b", help="Escala para azul")
argumento = analizador.parse_args()

#abriendo archivos
archivo=os.open(argumento.file, os.O_RDWR)
azul=os.open('azul.ppm', os.O_RDWR|os.O_APPEND)
verde=os.open('verde.ppm', os.O_RDWR|os.O_APPEND)
rojo=os.open('rojo.ppm', os.O_RDWR|os.O_APPEND)

#informacion del encabezado
off,ancho,alto,profundidad=cabecera.leer_cabecera(argumento.file)

#creando pipes
parent0,child0=mp.Pipe()
parent1,child1=mp.Pipe()
parent2,child2=mp.Pipe()

def h1(child):
    while True:
        print('reciviendo bloque...')
        recivir=child.recv()
        cadena=bytearray(recivir)
        pos=0
        pos1=2
        green=1
        i=0
        while i <= int((len(cadena)/3))-1:
            cadena[pos]=0
            cadena[pos1]=0
            numero=cadena[green]*validar_argumentos(argumento.g)
            try:
                cadena[green]=int(numero)
            except ValueError:
                cadena[green]=255
            pos+=3
            pos1+=3
            green+=3
            i+=1

        os.write(verde, cadena)
        if len(recivir) < int(argumento.size):
            break
    child.close()
    return

def h2(child):
    while True:
        print('reciviendo bloque...')
        recivir=child.recv()
        cadena=bytearray(recivir)
        pos=1
        pos1=2
        red=0
        i=0
        while i <= int((len(cadena)/3))-1:
            cadena[pos]=0
            cadena[pos1]=0
            numero=cadena[red]*validar_argumentos(argumento.r)
            try:
                cadena[red]=int(numero)
            except ValueError:
                cadena[red]=255
            pos+=3
            pos1+=3
            red+=3
            i+=1

        os.write(rojo, cadena)
        if len(recivir) < int(argumento.size):
            break
    child.close()
    return

def h3(child):
    while True:
        print('reciviendo bloque...')
        recivir=child.recv()
        cadena=bytearray(recivir)
        pos=0
        pos1=1
        blue=2
        i=0
        while i <= int((len(cadena)/3))-1:
            cadena[pos]=0
            cadena[pos1]=0
            numero=cadena[blue]*validar_argumentos(argumento.b)
            try:
                cadena[blue]=int(numero)
            except ValueError:
                cadena[blue]=255
            pos+=3
            pos1+=3
            blue+=3
            i+=1

        os.write(azul, cadena)
        if len(recivir) < int(argumento.size):
            break
    child.close()
    return

print('Creando hijos...')
p1=mp.Process(target=h1, args=(child0,))
p2=mp.Process(target=h2, args=(child1,))
p3=mp.Process(target=h3, args=(child2,))

#ejecutando hijos
p1.start()
p2.start()
p3.start()

#copiar cabecera
leer=os.read(archivo, off)
os.write(verde, leer)
os.write(rojo, leer)
os.write(azul, leer)

while True:
    print('leyendo bloque...')
    leer=os.read(archivo, int(argumento.size))
    parent0.send(leer)
    parent1.send(leer)
    parent2.send(leer)
    if len(leer) < int(argumento.size):
        break
p1.join()
p2.join()
p3.join()

#cerrando lo usado
parent0.close()
child0.close()
parent1.close()
child1.close()
parent2.close()
child2.close()
os.close(archivo)
os.close(azul)
os.close(verde)
os.close(rojo)

print('Copia exitosa...')
