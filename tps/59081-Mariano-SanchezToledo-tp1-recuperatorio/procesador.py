#!/bin/python3

import os
import sys
import multiprocessing as mp
import argparse
import array
import time


def rojo(imageInt, header):
    global arrayRojo
    rojo = []
    pointer = -1
    for i in range(len(imageInt)):
        pointer += 1
        if pointer % 3 == 0:
            # *Lee el pixel de la lista y se le multiplica la intensidad seleccionada.
            red = int(imageInt[i] * args.red)
            if red > 255:
                red = 255

            rojo += [red] + [0] + [0]

    # *Agrego al array los valores de los pixeles
    arrayRojo = array.array('B', [i for i in rojo])

    # *Creo imagen correspondiente
    with open('rojo.ppm', 'wb', os.O_CREAT) as fd:
        fd.write(bytearray(header, 'ascii'))
        arrayRojo.tofile(fd)
        fd.close


def verde(imageInt, header):
    global arrayVerde
    verde = []
    pointer = -1
    for i in range(len(imageInt)):
        pointer += 1
        if pointer % 3 == 1:
            # *Lee el pixel de la lista y se le multiplica la intensidad seleccionada.
            green = int(imageInt[i] * args.green)
            if green > 255:
                green = 255

            verde += [0] + [green] + [0]

    arrayVerde = array.array('B', [i for i in verde])

    # *Creo imagen correspondiente
    with open('verde.ppm', 'wb', os.O_CREAT) as fd:
        fd.write(bytearray(header, 'ascii'))
        arrayVerde.tofile(fd)
        fd.close


def azul(imageInt, header):
    global arrayAzul
    azul = []
    pointer = -1
    for i in range(len(imageInt)):
        pointer += 1
        if pointer % 3 == 2:
            # *Lee el pixel de la lista y se le multiplica la intensidad seleccionada.
            blue = int(imageInt[i] * args.blue)
            if blue > 255:
                blue = 255

            azul += [0] + [0] + [blue]

    arrayAzul = array.array('B', [i for i in azul])

    # *Creo imagen correspondiente
    with open('azul.ppm', 'wb', os.O_CREAT) as fd:
        fd.write(bytearray(header, 'ascii'))
        arrayAzul.tofile(fd)
        fd.close


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(
            description='Procesador de filtros de imagenes ppm.')
        parser.add_argument('-f', '--file', type=str,
                            help='Indique ruta de archivo.')
        parser.add_argument('-n', '--num', type=int,
                            help='Indique cantidad de bytes por bloques para lectura.')
        parser.add_argument('-r', '--red', type=float,
                            help='Intensidad de color rojo.')
        parser.add_argument('-g', '--green', type=float,
                            help='Intesidad color verde.')
        parser.add_argument('-b', '--blue', type=float,
                            help='Intensidad color azul.')
        args = parser.parse_args()

            # *Padre lee archivo
        print('=========COMENZANDO LECTURA========')
        print('Leyendo imagen de a bloques de', args.num, 'bytes')
        imagen = open(args.file, 'rb').read()

            # *Elimino comentarios
        for num in range(imagen.count(b'\n# ')):
            com1 = imagen.find(b'\n# ')
            com2 = imagen.find(b'\n', com1 + 1)
            imagen = imagen.replace(imagen[com1:com2], b'')

        findHeader = imagen.find(b'\n', imagen.find(b'\n', imagen.find(b'\n') + 1) + 1) + 1

            # *Guardo header y body
        header = imagen[:findHeader].decode()
        body = imagen[findHeader:]

        # *Paso los pixeles a int
        imageInt = [i for i in body]

        time.sleep(2)
        print('Lectura finalizada con exito\n')
    except:
        print('Error al leer el archivo, verifique los parametros ingresados')
        sys.exit(1)

    # *Creo hijos
    try:
        print('===========CREANDO HIJOS=============')
        proceRojo = mp.Process(target=rojo(imageInt, header), args=())
        proceVerde = mp.Process(target=verde(imageInt, header), args=())
        proceAzul = mp.Process(target=azul(imageInt, header), args=())
        print('Hijos creados con exito...\n')

        proceRojo.start()
        proceVerde.start()
        proceAzul.start()

        proceRojo.join()
        proceVerde.join()
        proceAzul.join()

    except:
        print('Error al crear los hijos, verifique los parametros ingresados')
        sys.exit(1)

    print('===========GENERANDO BONUS==============')
    try:
        time.sleep(2)
        bonus = []
        pointer = -1

        ''' Leo el dato necesario de cada array anterior segun indique el pointer
        y lo agrego a una lista llamada bonus'''

        for i in range(len(imageInt)):
            pointer += 1
            if pointer % 3 == 0:
                r = arrayRojo[i]
                bonus += [r]
            elif pointer % 3 == 1:
                g = arrayVerde[i]
                bonus += [g]
            elif pointer % 3 == 2:
                b = arrayAzul[i]
                bonus += [b]

        # *Creo array para bonus.
        arrayBonus = array.array('B', [i for i in bonus])

        # *Reconstruyo la imagen.
        with open('reconstruccion.ppm', 'wb', os.O_CREAT) as fd:
            fd.write(bytearray(header, 'ascii'))
            arrayBonus.tofile(fd)
            fd.close

        print('Bonus realizado con exito...\n')

    except:
        print('Error al realizar el bonus, vuelva a intentarlo mas tarde')
        sys.exit(1)
