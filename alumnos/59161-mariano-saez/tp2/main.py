#!/usr/bin/env python3
import argparse
import threading as th
import os
import errores
import sys
import re
import mmap
from worker import Worker


# ===================== PPM ROTOR ============================

# Funcion encargada de abrir el fd para la imagen .ppm
#   @path: Path de la imagen a procesar
def open_image(path: str):
    # Intentar abrir el archivo
    try:
        if path.endswith('.ppm') or\
           len(path.split('.')) == 1:
            fd = os.open(f'{path}', os.O_RDWR)
        else:
            raise errores.InvalidFileExtension

    # Manejar un par de excepciones por las dudas
    except errores.InvalidFileExtension:
        print(f'Extension de archivo invalida')
        sys.exit(1)
    except FileNotFoundError:
        print(f'Archivo {path} no encontrado')
        sys.exit(1)
    except Exception as e:
        print(f'Error inesperado abriendo {path}. Error {e}')
        sys.exit(1)

    return fd


# Funcion encargada de encontrar el principio del payload
#   @img: Imagen mapeada a memoria
def seek_payload(m_space: mmap):
    cursor = 0
    header = ''
    regex = r"(#.*\n)*(P6|P3)(\n|\s){0,2}(#.*\n)*(\d+)(\n|\s){0,2}(#.*\n)*(\d+)(\n|\s){0,2}(#.*\n)*(255|1023)(\n|\s){0,2}(#.*\n)*"
    while not re.match(regex, header, re.MULTILINE):
        try:
            header += str(m_space.readline(), encoding='utf-8')
            
            # Esta condicion se cumple cuando se llego al final del la memoria
            # mapeada y no se es capaz de avanzar.
            if cursor == m_space.tell():
                raise errores.FormatIdentifierNotFound
            cursor = m_space.tell()

        except errores.FormatIdentifierNotFound:
            print("El archivo no contiene la cabecera de una archivo PPM")
            sys.exit(1)

        except Exception as e:
            print(f'Error inesperado leyendo el archivo. Error {e}')
            sys.exit(1)

    return cursor, header


# Funcion encargada de crear una imagen rotada en DISCO
#   @header: Header de la imagen a rotar
#   @name: Nombre del archivo [para nombrar el nuevo]
def gen_file(header: str, name: str, sentido: int):
    # Crear imagen en disco
    try:
        if sentido == 90:
            fd_img = os.open(f'r_{name}', os.O_CREAT | os.O_RDWR)
        else:
            fd_img = os.open(f'l_{name}', os.O_CREAT | os.O_RDWR)
    except Exception as e:
        print(f'Error inesperado al crear imagen rotada. {e}')
        sys.exit(1)

    # Encontrar dimensiones del archivo ppm
    regex = r'(#.*\n)*(P6|P3)(\n|\s){0,2}(#.*\n)*(\d+)(\n|\s){0,2}(#.*\n)*(\d+)(\n|\s){0,2}'
    header_cortado = re.search(regex, header)[0]
    splited_header = re.split('\n| ', header_cortado)
    new_wide, new_high = int(splited_header[-3]), int(splited_header[-2])

    # Generar el header y crear el archivo nuevo
    new_header = f'P6\n{new_high} {new_wide}\n255\n'
    os.write(fd_img, bytes(new_header, 'utf-8'))

    # Crear matriz rotada
    matrix = [[[0, 0, 0] for i in range(new_high)] for j in range(new_wide)]

    return fd_img, len(new_header), matrix, new_wide, new_high


# Guarda la matriz en disco por filas, es decir, si la matriz de
# k filas * n columnas, se realizaran k syscalls a write
def dump_matrix(dump_fd, matrix):
    for i in matrix:
        dump_buff = b''
        for j in i:
            # En lugar de un tercer bucle usar indexacion
            # reduce el tiempo de rotacion de code.ppm [1.7MB]
            # de 2m16,041s a 1m20,580s
            # for k in j:
            #     dump_buff += bytes([k])
            dump_buff += bytes([j[0], j[1], j[2]])
        os.write(dump_fd, dump_buff)


# Funcion de prueba para ver la matriz
def print_matrix(matrix):
    for i in matrix:
        print(f"{i}")


if __name__ == "__main__":
    # Tomamos los argumentos [CLI]
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file',
                        metavar='FILE',
                        help='Archivo a procesar',
                        required=True)
    parser.add_argument('-s', '--size',
                        metavar='SIZE',
                        help='Bloque de lectura',
                        type=int,
                        required=True)
    parser.add_argument('--sentido',
                        metavar='SENTIDO',
                        help='Sentido de rotacion',
                        type=int,
                        required=False,
                        default=-90)
    args = parser.parse_args()

    if args.size < 3:
        args.size = 3
    else:
        args.size = args.size - args.size % 3

    # Lista de fd para cerrarlos mas facil
    fd_list = list()

    # Se abre el archivo con manejo de errores
    fd = open_image(f'{args.file}')
    fd_list.append(fd)

    # Mapear imagen a memoria, posicionarse en el payload y obtener
    # el header
    m_img = mmap.mmap(fd, 0)
    inicio_pl, header = seek_payload(m_img)
    m_img.close()

    # Crear el archivo donde se va a volcar y la matriz transpuesta
    rot_fd, start, matrix, width, high = gen_file(header, args.file, args.sentido)
    fd_list.append(rot_fd)

    # Pararnos en el comienzo del ruster
    os.lseek(fd, inicio_pl, 0)

    # Buffer de lectura
    buff = list(b'\x00')

    # Barrier para sincronizacion
    b1 = th.Barrier(4)

    # Instanciar trabajadores de cada color [RGB]
    workers = list()
    for i in range(3):
        try:
            worker = Worker(i, width, high, matrix, buff, b1, args.size, args.sentido)
            workers.append(worker)
        except th.ThreadError as e:
            print(f'Error al crear hilos de trabajo. {e}')
            for i in fd_list:
                os.close(i)
            sys.exit(1)

    # Variables de control
    ruster_sz = width*high*3
    read_bytes = 0

    # Leer por chunks el archivo
    while True:
        # Cargar el buffer
        chunk = os.read(fd, args.size)
        buff[0] = chunk

        # Bytes leidos
        read_bytes += len(chunk)

        # Comprobar el caso que termine con \n
        if len(buff[0]) % 3 != 0:
            buff[0] = buff[0][:-1]

        # En caso de ser la 1er iteracion activar los hilos
        if not workers[0].is_alive():
            for i in workers:
                i.start()

        # 1er barrier para indicar que ya se cargo el buffer
        b1.wait()

        if len(buff[0]) < args.size and read_bytes >= ruster_sz:
            break

        # 2do barrier esperar que todos terminen de leer
        b1.wait()

    # Tareas del hogar

    # Esperamos a los hilos
    for i in workers:
        i.join()

    # Volcamos a disco lo procesado
    dump_matrix(rot_fd, matrix)

    for i in fd_list:
        os.close(i)

    print(f"Imagen rotada {args.sentido} grados con exito!")

    sys.exit(0)
