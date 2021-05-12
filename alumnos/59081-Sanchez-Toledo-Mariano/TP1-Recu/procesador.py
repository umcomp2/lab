#!/bin/python3

import os
import multiprocessing as mp
import argparse
import array
import time


def getHeader():
    #Crea una lista con los datos del Header de la imagen.
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

'''
Ver como solucionar la lectura por bloques ya que no esta implementado...
'''


def getBody():
    #* Obtiene el body
    fd = open(args.file, 'rb').read()
    finheader = fd.find(b"\n", fd.find(b"\n", fd.find(b"\n") + 1) + 1) + 1
    body = fd[finheader:]
    body = array.array('B', [i for i in body])
    return body


def splitBody(body):
    #* Lee Body y lo separa en 3 Queues segun color.
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

def rojo(header):
    rojo = []
    fd = open('rojo.ppm', 'w')
    fd.write('{}\n{} {}\n{}\n'.format(header[0], header[1], header[2], header[3]))
    while True:
        #*Pasa cada valor de la Queue a la lista rojo.
        getQueue = queueRed.get()
        rojo.append(getQueue) 
        if queueRed.qsize() == 0 or queueRed.qsize() is None:
            break
    #!BORRAR
    print(rojo)
    
    '''for i in rojo:
        fd.write(i)
        fd.write(0)
        fd.write(0)'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help='Indique ruta archivo')
    parser. add_argument('-n', '--num', type=int,
                         help='Indique cantidad de bytes por bloque')
    args = parser.parse_args()

    #try:
    print('\n====Leyendo Archivo====\n')
    header = getHeader()
    print('Header obtenido...')
    queueRed = mp.Queue()
    queueGreen = mp.Queue()
    queueBlue = mp.Queue()
    print('Queues creadas...')
    print('\nArchivo Leído Correctamente\n')
    print('Iniciando recontruccion de imagen ppm...')

    #except:
        #print('\nError al leer Archivo, por favor verifica la ruta del archivo .ppm.\n')
        #exit(2)

    proceRojo = mp.Process(target=rojo(header), args=(queueRed))
    proceRojo.start()
    proceRojo.join()

    exit(0)
