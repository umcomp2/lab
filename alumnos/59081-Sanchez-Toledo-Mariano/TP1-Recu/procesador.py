#!/bin/python3

import os
import multiprocessing as mp
import argparse
import array


def getHeader():
    contador = 0
    # Crea una lista con los datos del Header de la imagen.
    fd = open(args.file, 'r')
    header = []
    datos = os.read(fd, 50).split()
    for i in datos:
        if i == b'P6':
            header.append(i)
        elif i.isdigit():
            header.append(i)
        else:
            pass
    os.close(fd)
    return header


def rojo(header):
    rojo = []
    pointer = 0
    # Obtiene body y lo guarda en un array.
    fd = open(args.file, 'rb')
    data = fd.read()
    finheader = data.find(b"\n", data.find(b"\n", data.find(b"\n") + 1) + 1) + 1
    body = data[finheader:]
    body = array.array('B', [i for i in body])
    fd.close()

    # Lee Body y guarda lo correspondiente al colo rojo.
    for i in body:
        if pointer % 3 == 0:
            queueRed.put(i)
        else:
            pass
        pointer += 1

    # Comienza el rearmado de la imagen.
    fd = open('rojo.ppm', 'w')
    fd.write('{}\n{} {}\n{}\n'.format(str(header[0]), str(
        header[1]), str(header[2]), str(header[3])))

    # Pasar cada valor de queue a lista correspondiente
    while True:
        getQueue = queueRed.get()
        rojo.append(getQueue)
        if queueRed.qsize() == 0 or queueRed.qsize() is None:
            break

    for i in rojo:
        # Ver tema de la intensidad (esta omitido para probar)
        pointer += 1
        fd.write(i, '')
        while range(0, 1):
            fd.write(0, '')
        if pointer == 4:
            fd.write('\n')
        else:
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help='Indique ruta archivo')
    parser. add_argument('-n', '--num', type=int,
                         help='Indique cantidad de bytes por bloque')
    args = parser.parse_args()

    try:
        print('\n====Leyendo Archivo====\n')
        header = getHeader()
        queueRed = mp.Queue()
        queueGreen = mp.Queue()
        queueBlue = mp.Queue()
        print('\nArchivo Leído Correctamente\n')

    except:
        print('\nError al leer Archivo, por favor verifica la ruta del archivo .ppm.\n')
        exit(2)

    proceRojo = mp.Process(target=rojo(header), args=(queueRed,))
    #proceVerde = mp.Process(target=verde(), args=(queueGreen,))
    #proceAzul = mp.Process(target=azul(), args=(queueBlue,))

    proceRojo.start()
    # proceVerde.start()
    # proceAzul.start()

    proceRojo.join()
    print('Proceso Rojo finalizo correctamente')
    # proceVerde.join()
    #print('Proceso Verde finalizo correctamente')
    # proceAzul.join()
    #print('Proceso Azul finalizo correctamente')

    print('Error al generar procesos')
    exit(2)

    exit(0)
