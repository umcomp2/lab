import sys
import argparse
from pathlib import Path
import os
from threading import Barrier as barr
from itertools import chain
import array
import threading


WEIGHT = 0
HEIGHT = 0
MAXVAL = 0
PUNTERO = 0
STOP = 0


def eliminar_header(image):
    global WEIGHT, HEIGHT, MAXVAL, PUNTERO
    ppm = open(image, encoding='latin1').read()
    header_data = [ppm[:2]]
    in_comment = False
    current_value = ''
    for n, c in enumerate(ppm[2:], 2):
        if len(header_data) == 4:
            header_data.append(n)
            break
        if in_comment:
            if c == '\n':
                in_comment = False
        elif c == '#':
            in_comment = True
        elif c.isspace():
            if current_value:
                header_data.append(int(current_value))
                current_value = ''
        elif c.isdigit():
            current_value += c
    WEIGHT = header_data[1]
    HEIGHT = header_data[2]
    MAXVAL = header_data[3]
    sub_char = str(header_data[3])
    indexs = ppm.index(sub_char)
    PUNTERO = (indexs+4)


def gen_matrix():
    global WEIGHT, HEIGHT
    matrix_g = []
    for _ in range(0, WEIGHT*HEIGHT):
        matrix_g.append([[], [], []])
    return matrix_g


def make_mirroring(pixels_rgb, color, bar, matrix_g):
    global WEIGHT, HEIGHT, STOP
    while True:
        bar.wait()
        STOP = 0
        columnas = WEIGHT
        # Me paro en la ultima columna
        puntero = columnas-1
        # Variable necesaria para siempre ubicarse al final de la fila
        salto = puntero
        # Contador para modificar el valor del puntero y la variable salto
        contador = 0
        for i in pixels_rgb[color::3]:
            # Guardo el valor de la lista_t en la matriz empezando desde el final y terminando al principio
            try:
                matrix_g[puntero][color] = i
            except IndexError:
                STOP = 1
            contador += 1
            # Primero me ubico en la ultima fila de la matriz vacia y luego voy yendo hacia al principio de la fila
            puntero -= 1
            if contador == columnas:
                contador = 0
                salto += columnas
                puntero = salto
        if len(pixels_rgb) == (WEIGHT*HEIGHT*3):
            break
        bar.wait()
        if STOP > 0:
            break


def main():
    global WEIGHT, HEIGHT, MAXVAL, PUNTERO, STOP
    parser = argparse.ArgumentParser('Leer imagen PPM')
    parser.add_argument('-s',
                        '--size',
                        help='La cantidad de bytes a leer',
                        required=True,
                        action='store',
                        type=int)
    parser.add_argument('-f',
                        '--file',
                        help='PPM a leer',
                        required=True,
                        action='store',
                        type=str)

    args = parser.parse_args()
    try:
        print('Iniciando...')
        if args.size:
            numero = int(args.size)

            # Deteccion de errores

            if numero < 3:
                print('El numero debe ser multiplo de 3 o igual a 3')
                sys.exit()
            if args.file:
                tamaño_archivo = Path(args.file).absolute()
                tamaño = os.path.getsize(tamaño_archivo)
                if numero > tamaño:
                    print(f'El tamaño a leer debe ser menor al tamaño del archivo.'
                          f'\nNumero introducido: {numero} > Tamaño del archivo: '
                          f'{tamaño}')
                    sys.exit()
                imagen = args.file
                if 'ppm' not in imagen:
                    print('Error, La imagen debe ser de formato PPM')
                    sys.exit()

                # Lectura de Header y Creacion de Matriz vacia

                eliminar_header(imagen)
                bar = barr(4)

                matrix_g = gen_matrix()
                pixels_rgb = []
                colores = [0, 1, 2]
                thrds = []
                for i in colores:
                    thr = threading.Thread(target=make_mirroring, args=(
                        pixels_rgb, colores[i], bar, matrix_g))
                    thrds.append(thr)
                apertura_arc = os.open(imagen, os.O_RDONLY)
                os.lseek(apertura_arc, PUNTERO, 0)
                while True:
                    f_read = os.read(apertura_arc, numero)
                    for i in f_read:
                        pixels_rgb.append(i)
                    for i in thrds:
                        if i.is_alive() == False:
                            i.start()
                    bar.wait()
                    if len(pixels_rgb) == (WEIGHT*HEIGHT*3):
                        break
                    bar.wait()
                    if STOP > 0:
                        break
                for i in thrds:
                    i.join()
                print('Finalizando...')
                z = 0
                x = 1
                y = 2
                matrix_g = list(chain(*matrix_g))
                ppm_header = f'P6\n{WEIGHT} {HEIGHT}\n{MAXVAL}\n'
                with open(f'{imagen}_mirroring.ppm', 'wb') as f:
                    f.write(bytearray(ppm_header, 'ascii'))
                    while True:
                        try:
                            image = array.array(
                                'B', [matrix_g[z], matrix_g[x], matrix_g[y]])
                            z += 3
                            x += 3
                            y += 3
                            image.tofile(f)
                        except IndexError:
                            break

    except FileNotFoundError as error:
        print(error)


if __name__ == '__main__':
    main()
