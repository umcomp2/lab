#!/bin/python3

import os
import sys
import time
import multiprocessing as mp
import argparse
import array


varPadre, varHijo = mp.Pipe()


def getHeader():
    header = []
    fd = os.open(args.file, os.O_RDONLY)
    datos = os.read(fd, 50).split()
    for i in datos:
        if i == b'P6':
            header.append(i)
        elif i.isdigit():
            header.append(i)
        else:
            pass
    return header


def getBody():
    fd = open(args.file, 'rb').read()
    finheader = fd.find(b"\n", fd.find(b"\n", fd.find(b"\n") + 1) + 1) + 1
    body = fd[finheader:]
    body = array.array('B', [i for i in body])
    return body


def splitBody(body):
    pointer = -1
    for i in body:
        pointer += 1
        if pointer % 3 == 0:
            queueRed.put(i)
        elif pointer % 3 == 1:
            queueGreen.put(i)
        elif pointer % 3 == 2:
            queueBlue.put(i)
        else:
            break


def rojo():
    rojo = []
    fd = open('rojo.txt', 'w')
    fd.write('Histograma color Rojo')
    while True:
        #Pasa cada valor de la Queue a la lista rojo
        getQueue = queueRed.get()
        rojo.append(getQueue) 
        if queueRed.qsize() == 0 or queueRed.qsize() is None:
            break
    for i in range(256):
        #Escribe en el archivo el valor y la frecuencia
        fd.write('Valor: {}, Frecuencia: {}\n'.format(i, rojo.count(i)))



def verde():
    verde = []
    fd = open('verde.txt', 'w')
    fd.write('Histograma color Verde')
    while True:
        #Pasa cada valor de la Queue a la lista verde
        getQueue = queueGreen.get()
        verde.append(getQueue) 
        if queueGreen.qsize() == 0 or queueGreen.qsize() is None:
            break
    for i in range(256):
        #Escribe en el archivo el valor y la frecuencia
        fd.write('Valor: {}, Frecuencia: {}\n'.format(i, verde.count(i)))


def azul():
    azul = []
    fd = open('azul.txt', 'w')
    fd.write('Histograma color Azul')
    while True:
        #Pasa cada valor de la Queue a la lista azul
        getQueue = queueBlue.get()
        azul.append(getQueue) 
        if queueBlue.qsize() == 0 or queueBlue.qsize() is None:
            break
    for i in range(256):
        #Escribe en el archivo el valor y la frecuencia
        fd.write('Valor: {}, Frecuencia: {}\n'.format(i, azul.count(i)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help='Indique ruta archivo')
    parser. add_argument('-n', '--num', type=int, help='Indique cantidad de bytes por bloque')
    args = parser.parse_args()

    try:
        print('\n====Leyendo Archivo====\n')
        header = getHeader()
        body = getBody()
        head = ('MagicNumber: {}\nAncho: {}\nAlto: {}\nmaxVal: {}\n'.format(
            str(header[0]), str(header[1]), str(header[2]), str(header[3])))
        print(head)
        queueRed = mp.Queue()
        queueGreen = mp.Queue()
        queueBlue = mp.Queue()
        splitBody(body)
        print('\nArchivo Leído Correctamente\n')
        time.sleep(2)
        
    except:
        print('\nError al leer Archivo, por favor verifica la ruta del archivo .ppm.\n')
        exit(2)

    try:
        proceRojo = mp.Process(target=rojo(), args=(queueRed,))
        proceVerde = mp.Process(target=verde(), args=(queueGreen,))
        proceAzul = mp.Process(target=azul(), args=(queueBlue,))

        proceRojo.start()
        proceVerde.start()
        proceAzul.start()

        proceRojo.join()
        print('Proceso Rojo finalizo correctamente')
        proceVerde.join()
        print('Proceso Verde finalizo correctamente')
        proceAzul.join()
        print('Proceso Azul finalizo correctamente')

    except:
        print('Error al generar procesos')
        exit(2)
    
    exit(0)
