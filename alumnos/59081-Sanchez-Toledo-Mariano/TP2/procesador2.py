#!/bin/python3

import os
import sys
import numpy as np
import threading
import argparse
import array
import time

from numpy.core.numeric import argwhere


def rojo(imageInt):
    global superbody
    superbody = []
    pointer = -1
    for i in range(len(imageInt)):
        pointer += 1
        if pointer % 3 == 0:
            red = int(imageInt[i])
            superbody.insert(i, red)

def verde(imageInt):
    pointer = -1
    for i in range(len(imageInt)):
        pointer += 1
        if pointer % 3 == 1:
            green = int(imageInt[i])
            superbody.insert(i, green)

def azul(imageInt, header):
    pointer = -1
    for i in range(len(imageInt)):
        pointer += 1
        if pointer == 2:
            blue = int(imageInt[i])
            superbody.insert(i, blue)
    
    time.sleep(5)
    #newbody = [superbody[i:i + 3] for i in range(0, len(superbody), 3)]
    superarray = np.array(superbody)

    

    with open('rotada.ppm', 'wb', os.O_CREAT) as fd:
        fd.write(bytearray(header, 'ascii'))
        superarray.tofile(fd)
        fd.close()

'''
        HAY UN ERROR EN LAS FUNCIONES DE LAS THREADS, NO SE REARMA BIEN LA IMAGEN
'''






if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Rotador de imagenes ppm!!')
        parser.add_argument('-f', '--file', type=str,
                            help='Indique la ruta del archivo')
        parser.add_argument('-n', '--num', type=int,
                            help='Indique tamaño de bloque de lectura')
        args = parser.parse_args()

        # *Padre lee archivo
        print('=========COMENZANDO LECTURA========')
        imagen = open(args.file, 'rb').read()

        # *Elimino comentarios
        for num in range(imagen.count(b'\n# ')):
            com1 = imagen.find(b'\n# ')
            com2 = imagen.find(b'\n', com1 + 1)
            imagen = imagen.replace(imagen[com1:com2], b'')

        findHeader = imagen.find(b'\n', imagen.find(
            b'\n', imagen.find(b'\n') + 1) + 1) + 1

        # *Guardo header y body
        header = imagen[:findHeader].decode()
        body = imagen[findHeader:]
        #listheader = header.split()
        #header = ''.join(listheader[0] + '\n' + listheader[2] + ' ' + listheader[1] + '\n' + listheader[3] + '\n')

        # *Paso los pixeles a int
        imageInt = [i for i in body]

        time.sleep(2)
        print('Lectura finalizada con exito\n')
    except:
        print('Error al leer el archivo, verifique la ruta')
        sys.exit(1)


    threadRojo = threading.Thread(target=rojo(imageInt), args=())
    threadVerde = threading.Thread(target=verde(imageInt), args=())
    threadAzul = threading.Thread(target=azul(imageInt, header), args=())

    threadRojo.start()
    threadVerde.start()
    threadAzul.start()

    threadRojo.join()
    threadVerde.join()
    threadAzul.join()