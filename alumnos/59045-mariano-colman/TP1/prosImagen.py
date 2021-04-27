#!/usr/bin/python3

import argparse
import multiprocessing as mp
import os
from queue import Empty
import matplotlib.pyplot as plt
import time
import sys


def padre(args, hRojo, hVerde, hAzul):
    try:
        print("Soy el proceso padre, PID:", os.getpid(), "comienzo a leer la imagen....")
        
        #arch = os.open(args.file, os.O_RDONLY)
        #img = os.read(arch, args.size)

        #Abro la imagen y la leo en bytes
        img = open(args.file, "rb").read()

        #Con la imagen abierta procedo a reemplazar los comentarios
        for i in range(img.count(b"\n# ")):
            basura1 = img.find(b"\n# ")
            basura2 = img.find(b"\n", basura1 + 1)
            img = img.replace(img[basura1:basura2], b"")
        
        img.close()
        #Calculo la posicion donde se encuentra la delimitacion del header con el body
        limiteHeader = img.find(b"\n", img.find(b"\n", img.find(b"\n")+1)+1)+1

        
        header = img[:limiteHeader].decode()
        body = img[limiteHeader:]

        #Genero un archivo body para poder manipularlo
        archivo = os.open("body.txt", os.O_WRONLY)
        os.write(archivo, body)

        #Leo por bloques y los agrego a las colas de procesamiento
        l = b''
        fd = os.open("body.txt", os.O_RDONLY)
        while True:
            leido = os.read(fd, args.size)
            l += leido
            colaR.put(leido)
            colaV.put(leido)
            colaA.put(leido)
            if len(leido) != args.size:
                break
        os.close(fd)
        print(body == l)

        print("Imagen procesada!")

        #Corro los hijos y espero a que terminen con join 
        hRojo.start()
        hVerde.start()
        hAzul.start()

        hRojo.join()
        hVerde.join()
        hAzul.join()

        #El padre espera a la finalizacion de cada hijo y emite un mensaje de que fue resuelto con exito
        print("\nHistograma realizado!")
    except IOError:
        print("\nEl nombre del archivo ingresado es incorrecto")


#Creo tres funciones, cada una va a extraer la intensidad de su color, genera un archivo y por ultimo un histograma
def colorRojo(cola):
    time.sleep(2)
    print("Hijo color rojo - PID's:", os.getpid(), os.getppid())
    rojo = []
    j = 0
    while True:
        try:
            bloque = cola.get_nowait()
            for i in range(len(bloque)):
                if i % 3 == 0 or i == 0:
                    valRojo = int(bloque[i])
                    rojo.append(valRojo)
                    j += 1
        except Empty as e:
            break

    #histograma
    valores = ' '.join(str(rojo))
    archivo = open("rojo.txt", "w")
    archivo.write(valores)
    plt.hist(rojo, rwidth=0.9, bins=50)
    plt.xlabel('Valor de pixel')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de valores del color rojo')
    plt.show()


def colorVerde(cola):
    time.sleep(2)
    print("Hijo color verde - PID's:", os.getpid(), os.getppid() )
    verde = []
    j = 0
    while True:
        try:
            bloque = cola.get_nowait()
            for i in range(len(bloque)):
                if (i+2) % 3 or i == 1:
                    valVerde = int(bloque[i])
                    verde.append(valVerde)
                    j += 1
        except Empty:
            break

    #histograma
    valores = ' '.join(str(verde))
    archivo = open("verde.txt", "w")
    archivo.write(valores)
    plt.hist(verde, rwidth=0.9, bins=50)
    plt.xlabel('Valor de pixel')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de valores del color verde')
    plt.show()

def colorAzul(cola):
    time.sleep(2)
    print("Hijo color azul - PID's:", os.getpid(), os.getppid())
    j = 0
    azul = []
    while True:
        try:
            bloque = cola.get_nowait()
            for i in range(len(bloque)):
                if (i+1) % 3 or i == 2:
                    valAzul = int(bloque[i])
                    azul.append(valAzul)
                    j += 1
        except Empty:
            break
    valores = ' '.join(str(azul))
    archivo = open("azul.txt", "w")
    archivo.write(valores)

    #histograma
    plt.hist(azul, rwidth=0.9, bins=50)
    plt.xlabel('Valor de pixel')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de valores del color azul')
    plt.show()

if __name__ == '__main__':

    try:
        parser = argparse.ArgumentParser(description="Procesamiento de imagenes por colores")

        parser.add_argument("-f", "--file", type=str, required=True, help="Nombre de la imagen")
        parser.add_argument("-s", "--size", type=int, default=1024, help="Valor del bloque a analizar")

        args = parser.parse_args()
    except:
        print("Valores ingresados incorrectos")
        sys.exit()
    try:
        if args.size <= 0:
            raise ValueError()
    except:
        print("Tamaño de bloque incorrecto")
        sys.exit()

#Creo las colas y defino los hijos
    colaR = mp.Queue()
    colaV = mp.Queue()
    colaA = mp.Queue()


    hRojo = mp.Process(target=colorRojo, name="hRojo", args=(colaR, ))
    hVerde = mp.Process(target=colorVerde, name="hVerde", args=(colaV, ))
    hAzul = mp.Process(target=colorAzul, name="hAzul", args=(colaA, ))

    padre(args, hRojo, hVerde, hAzul)

