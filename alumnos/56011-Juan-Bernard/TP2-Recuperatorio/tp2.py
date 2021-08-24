#!/usr/bin/python3
import argparse
import array
import os
import re
import threading
import warnings


aviso = None
aviso_m = None
raster = None
ppm_mat_1 = []
ppm_mat_2 = []
barrier_r = threading.Barrier(4)
barrier_w = threading.Barrier(4)
barrier_m = threading.Barrier(4)
barrier_l = threading.Barrier(3)
lista1 = array.array('B')
# Función para obtener obtener argumentos
def argumentos():
    parser = argparse.ArgumentParser(description='TP2 - Imágenes ppm')
    parser.add_argument('-s', '--size', type=int, default=1035,
                        help='Tamaño del bloque de lectura (Debe ser un '
                        'múltiplo de 3)')
    parser.add_argument('-f', '--file', action='store', type=str,
                        required=True, help='Archivo de imagen')
    return parser.parse_args()


# Función para obtener información del header
def define_header(file, f_name):
    with open(file, 'rb') as imagen:
        bloque = imagen.read(256)
        hd_regex = re.compile(rb'(?:(?:P(?:3|6))|(?:^|\b)\d+\b)')
        # Escribo header en el nuevo archivo que estará espejado
        espejado = open('espejado_%s.ppm' % f_name, 'wb')
        espejado.write(b'%s\n' % hd_regex.findall(bloque)[0])
        espejado.write(b'%s %s\n' % (hd_regex.findall(bloque)[1], hd_regex.findall(bloque)[2]))
        espejado.write(b'%s\n' % hd_regex.findall(bloque)[3])
        espejado.close()
        # Obtengo la posición en la que finaliza el header (en un \n)
        for match in re.finditer(rb'\n', bloque):
            new_line = match.end()
        # Retorna posición del fin del header e info del mismo
        return new_line, int(hd_regex.findall(bloque)[1]), int(hd_regex.findall(bloque)[2])

# Rota la imagen 
def espejar(color, ancho, altura, limit):
    global aviso
    global aviso_m
    global raster
    global ppm_mat_1
    global ppm_mat_2
    global lista1
    # Se define el comienzo de la iteración en el raster según el color
    if color == 'r':
        start = 0
    elif color == 'g':
        start = 1
    elif color == 'b':
        start = 2
    position_1 = start
    position_2 = start
    minim = 0
    maxim = ancho*3
    while True:
        if aviso_m == 'Terminado':
            break
        barrier_r.wait()
        # Termina de copiar raster en array
        if aviso == 'Terminado':
            for i in range(start, len(raster), 3):
                if position_1 >= limit:
                    break
                if start == 0:
                    ppm_mat_1[position_1] = raster[i]
                if start == 1:
                    ppm_mat_1[position_1] = raster[i]
                if start == 2:
                    ppm_mat_1[position_1] = raster[i]
                position_1 = position_1 + 3
            # Procesa listas con nuevas posiciones
            while True:
                lista = ppm_mat_1[minim:maxim]
                if position_2 >= limit:
                    aviso_m = 'Terminado'
                    barrier_w.wait()
                    break
                for k in range(start, ancho*3, 3):
                    barrier_l.wait()
                    if k >= limit:
                        break
                    if start == 0:
                        lista1[(ancho*3-1)-k-2] = lista[k]
                    if start == 1:
                        lista1[(ancho*3-1)-k] = lista[k]
                    if start == 2:
                        lista1[(ancho*3-1)-k+2] = lista[k]
                    position_2 = position_2 + 3
                barrier_m.wait()
                minim = minim + ancho*3
                maxim = maxim + ancho*3
        # Copia información de raster en array
        else:
            for i in range(start, len(raster), 3):
                if position_1 >= limit:
                    break
                if start == 0:
                    ppm_mat_1[position_1] = raster[i]
                if start == 1:
                    ppm_mat_1[position_1] = raster[i]
                if start == 2:
                    ppm_mat_1[position_1] = raster[i]
                position_1 = position_1 + 3
            barrier_m.wait()
            barrier_w.wait()



if __name__ == '__main__':
    # Llamar a función para traer argumentos
    args = argumentos()

    # Obtener nombre sin extensión
    f_name = args.file.split('.')[0]

    # Chequear si el archivo existe y si la extensión es ppm
    try:
        if os.path.isfile(args.file) is False:
            raise FileNotFoundError
        if args.file.split('.')[1] != 'ppm':
            raise NameError
    except FileNotFoundError:
        print('El archivo ingresado no existe.')
        exit()
    except NameError:
        print('La extensión del archivo no es ppm.')
        exit()

    # Chequear si el size es negativo y múltiplo de tres
    if args.size < 0:
        raise ValueError('El tamaño del bloque debe ser un número positivo.')

    # Chequear si el size es múltiplo de 3
    if args.size % 3 != 0:
        warnings.warn('El tamaño del bloque no es un número '
                      'múltiplo de 3.', stacklevel=2)
        args.size = 3*round(args.size/3)
        print("\nEl tamaño de bloque se redondeó a %d.\n" % args.size)

    # Trabajar el encabezado
    header, ancho, altura = define_header(args.file, f_name)
    ppm_mat_1 = array.array('B', [0, 0, 0] * ancho * altura)
    ppm_mat_2 = array.array('B')
    limit = ancho * altura * 3

    # Crear los tres hilos que procesan cada color
    hilos = ['r', 'g', 'b']
    for i in hilos:
        i = threading.Thread(target=espejar, args=('%s' % i, ancho, altura, limit))
        i.start()

    # Leer y escribir archivo
    with open(args.file, 'rb') as imagen:
        imagen.seek(header)
        espejado = open('espejado_%s.ppm' % f_name, 'ab')
        while True:
            raster = imagen.read(args.size)
            if len(raster) != args.size:
                aviso = 'Terminado'
                barrier_r.wait()
                lista1 = array.array('B', [0] * ancho * 3)
                # Suma listas a nuevo array rotado
                while aviso_m != 'Terminado':
                    barrier_m.wait()
                    ppm_mat_2 = ppm_mat_2 + lista1
                barrier_w.wait()
                espejado.write(ppm_mat_2)
                imagen.close()
                espejado.close()
                break
            barrier_r.wait()
            barrier_m.wait()
            ppm_mat_2 = ppm_mat_2 + lista1
            barrier_w.wait()


    # Esperar a que terminen los hilos para mostrar un mensaje
    print('\nEl trabajo ha finalizado. La imagen se espejó horizontalmente.')
