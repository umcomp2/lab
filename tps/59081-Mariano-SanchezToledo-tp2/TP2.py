#!/bin/python3

import os
import array
from args import Parser
from queue import Queue, Empty
from threading import *
import time


def getHeader(args):
    global listheader
    imagen = open(args.file, 'rb').read()

    #Elimino comentarios
    for num in range(imagen.count(b'\n# ')):
        com1 = imagen.find(b'\n# ')
        com2 = imagen.find(b'\n', com1 + 1)
        imagen = imagen.replace(imagen[com1:com2], b'')

    #LLego al limite entre el header y el body
    limite = imagen.find(b'\n', imagen.find(b'\n', imagen.find(b'\n') + 1) + 1) + 1
    header = imagen[:limite].decode()
    listheader = header.split()
    header = ''.join(listheader[0] + '\n' + listheader[2] + ' ' + listheader[1] + '\n' + listheader[3] + '\n')
    print('Header done')
    return header

def getBody(args):
    global imageInt
    imagen = open(args.file, 'rb').read()

    #Elimino comentarios
    for num in range(imagen.count(b'\n# ')):
        com1 = imagen.find(b'\n# ')
        com2 = imagen.find(b'\n', com1 + 1)
        imagen = imagen.replace(imagen[com1:com2], b'')

    #LLego al limite entre el header y el body
    limite = imagen.find(b'\n', imagen.find(b'\n', imagen.find(b'\n') + 1) + 1) + 1
    body = imagen[limite:]
    imageInt = [i for i in body]
    print('Body Done')
    return body

def getQueue(body):
    #Genero un archivo body para poder manipularlo
    archivo = os.open("body.txt", os.O_WRONLY|os.O_CREAT)
    os.write(archivo, body)

    #Leo por bloques y los agrego a las colas de procesamiento
    indktor = b''
    fd = os.open("body.txt", os.O_RDONLY)
    pointer = -1
    while True:
        pointer += 1
        leido = os.read(fd, args.size)
        indktor += leido

        for i in leido:
            if pointer % 3 == 0:
               # qRed.put(leido)
                cola.put(leido)
            if pointer % 3 == 1:
               # qGreen.put(leido)
                cola.put(leido)
            if pointer % 3 == 2:
               # qBlue.put(leido)
                cola.put(leido)
        
        if len(indktor) == len(body):
            break

    os.close(fd)
    os.remove('body.txt')
    print("Imagen procesada!")

def hilo(cola, newbody):
    try:
        while True:
            try:
                thLock.acquire(timeout=0.5)
                print('paso 1', current_thread().getName())
                x = cola.get_nowait()
                y = cola.get_nowait()
                z = cola.get_nowait()
                newbody += [[[x, y, z]]]
                print('paso 2', current_thread().getName())
                thLock.release()
            except Empty as e:
                break
    except ThreadError:
        print('Error en ejecucion de Hilos')

def rotarMatriz(matriz):
    rotada = []
    for i in range(len(matriz[0])):
        rotada.append([])
        for j in range(len(matriz)):
            rotada[i].append(matriz[len(matriz)-1-j][i])
    return rotada


if __name__ == '__main__':
#===========================================================#
    args = Parser.parser()
    header = getHeader(args)
    body = getBody(args)
    width = int(listheader[1])
    height = int(listheader[2])
    matrix = array.array('B', [0,0,0] * width * height)
    #matrix = [] * width * height
    newbody = []
#===========================================================#
   # qRed = Queue()
   # qGreen = Queue()
   # qBlue = Queue()
    cola = Queue()
    thLock = Lock()
    getQueue(body)
#===========================================================#
    th1 = Thread(target=hilo, name='rojo', args=(cola, newbody))
    th2 = Thread(target=hilo, name='verde', args=(cola, newbody))
    th3 = Thread(target=hilo, name='azul', args=(cola, newbody))

    th1.start()
    th2.start()
    th3.start()

    th1.join()
    th2.join()
    th3.join()

    print('Threading Done')
#===========================================================#
    rotada = rotarMatriz(newbody)





    with open('rotada.ppm', 'wb', os.O_CREAT) as fd:
        fd.write(bytearray(header, 'ascii'))  
        for item in rotada:
            for i in item:
                for k in i:
                    fd.write(k)
