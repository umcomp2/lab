#!/usr/bin/python3
import argparse
import multiprocessing as mp
import os
import re
import warnings


# Función para obtener obtener argumentos
def argumentos():
    parser = argparse.ArgumentParser(description='TP1 - Imágenes ppm')
    parser.add_argument('-s', '--size', type=int, default=1035,
                        help='Tamaño del bloque de lectura (Debe ser un '
                        'múltiplo de 3)')
    parser.add_argument('-f', '--file', action='store', type=str,
                        required=True, help='Archivo de imagen')

    return parser.parse_args()


# Función para obtener información del header
def define_header(file):
    with open(file, 'rb') as imagen:
        bloque = imagen.read(256)
        hd_regex = re.compile(rb'(?:(?:P(?:3|6))|(?:^|\b)\d+\b)')
        print('\nIdentificador:', hd_regex.findall(bloque)[0].decode('utf-8'))
        print('Ancho:', hd_regex.findall(bloque)[1].decode('utf-8'))
        print('Alto:', hd_regex.findall(bloque)[2].decode('utf-8'))
        print('Profundidad:', hd_regex.findall(bloque)[3].decode('utf-8'))
        # Obtengo la posición en la que finaliza el header (en un \n)
        for match in re.finditer(rb'\n', bloque):
            new_line = match.end()
        print('Tamaño del header:', new_line)
        # Retorna posición del fin del header
        return new_line


# Función que crea los histogramas
def define_hist(queue, color, f_name):
    # Se define el comienzo de la iteración en el raster según el color
    if color == 'red':
        start = 0
    elif color == 'green':
        start = 1
    elif color == 'blue':
        start = 2
    # Crea diccionario para guardar Intensidad y Repeticiones
    d_color = dict()
    while True:
        raster = queue.get()
        if raster == 'Terminado':
            break
        for i in range(start, len(raster), 3):
            if raster[i] in d_color:
                d_color[raster[i]] += 1
            else:
                d_color[raster[i]] = 1
    # Escribe información del diccionario en un archivo de texto
    fd = os.open('h_%s_%s.txt' % (f_name, color), os.O_WRONLY | os.O_CREAT |
                 os.O_TRUNC)
    os.write(fd, b'Int\tRep\n')
    for i in sorted(d_color.keys()):
        data = str(i) + '\t' + str(d_color[i]) + '\n'
        os.write(fd, data.encode('utf-8'))
    os.close(fd)


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

    # Chequear si el size es negativo
    if args.size < 0:
        raise ValueError('El tamaño del bloque debe ser un número positivo.')

    # Chequear si el size es múltiplo de 3
    if args.size % 3 != 0:
        warnings.warn('El tamaño del bloque no es un número '
                      'múltiplo de 3.', stacklevel=2)
        args.size = 3*round(args.size/3)
        print("\nEl tamaño de bloque se redondeó a %d.\n" % args.size)

    # Crear tres colas para comunicación
    queue_r = mp.Queue()
    queue_g = mp.Queue()
    queue_b = mp.Queue()

    # Crear los tres procesos hijos
    p_red = mp.Process(target=define_hist, args=(queue_r, 'red', f_name,))
    p_green = mp.Process(target=define_hist, args=(queue_g, 'green', f_name,))
    p_blue = mp.Process(target=define_hist, args=(queue_b, 'blue', f_name, ))

    # Inicializar los hijos
    p_red.start()
    p_green.start()
    p_blue.start()

    # Trabajar el encabezado
    print(args.file)
    header = define_header(args.file)

    # Leer archivo
    with open(args.file, 'rb') as imagen:
        imagen.seek(header)
        while True:
            raster = imagen.read(args.size)
            queue_r.put(raster)
            queue_g.put(raster)
            queue_b.put(raster)
            if len(raster) != args.size:
                imagen.close()
                break

    # Avisar que finalizó la lectura
    queue_r.put('Terminado')
    queue_g.put('Terminado')
    queue_b.put('Terminado')

    # Esperar que terminen los hijos
    p_red.join()
    p_blue.join()
    p_red.join()

    print('\nEl trabajo ha finalizado. Tres archivos con histogramas han sido '
          'creados.')
