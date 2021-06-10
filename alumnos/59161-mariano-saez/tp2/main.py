#!/usr/bin/env python3
import argparse
import threading as th
import os
import errores
import sys
import re
import mmap


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
def gen_file(header: str, name: str):
    # Crear imagen en disco
    fd_img = os.open(f'left_{name}', os.O_CREAT | os.O_RDWR)

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

    return fd_img, len(new_header), matrix, new_wide


# Indice global
rglobal_index = 0
gglobal_index = 0
bglobal_index = 0
# Esta funcion se encarga de colocar los bytes del color correspondiente
# en cada elemento de l matriz que recibe por parametro
#   @matrix: Matriz en donde reemplazar los elementos
#   @color: Color que se reemplazara dentro de cada pixel
#       Rojo: 0
#       Verde: 1
#       Azul: 2
#   @buff: Buffer de donde leer los pixeles que reemplezan elementos
#          en la matriz
def rfill_matrix(matrix, color, buff, width):
    global rglobal_index
    for i in range(color, len(buff), 3):
        col = int(rglobal_index/width)
        row = width - rglobal_index % width - 1
        matrix[row][col][color] = buff[i]
        rglobal_index += 1


def gfill_matrix(matrix, color, buff, width):
    global gglobal_index
    for i in range(color, len(buff), 3):
        col = int(gglobal_index/width)
        row = width - gglobal_index % width - 1
        matrix[row][col][color] = buff[i]
        gglobal_index += 1


def bfill_matrix(matrix, color, buff, width):
    global bglobal_index
    for i in range(color, len(buff), 3):
        col = int(bglobal_index/width)
        row = width - bglobal_index % width - 1
        matrix[row][col][color] = buff[i]
        bglobal_index += 1


# Guarda la matriz en disco
# TODO: Escribir por chunks mientras se construye la matriz
#       podria ser una aproximacion valida?
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
                        required=False)
    args = parser.parse_args()

    args.size = args.size - (args.size % 3)

    # Se abre el archivo con manejo de errores
    fd = open_image(f'{args.file}')

    # Mapear imagen a memoria, posicionarse en el payload y obtener
    # el header
    m_img = mmap.mmap(fd, 0)
    inicio_pl, header = seek_payload(m_img)
    m_img.close()

    # Crear el archivo donde se va a volcar y la matriz transpuesta
    rot_fd, start, matrix, width = gen_file(header, args.file)
    
    # Pararnos en el comienzo del ruster
    os.lseek(fd, inicio_pl, 0)
    
    # Leer por chunks el archivo
    while True:
        buff = os.read(fd, args.size)

        # Comprobar el caso que termine con \n
        if len(buff) % 3 != 0:
            buff = buff[:-1]

        rfill_matrix(matrix, 0, buff, width)
        gfill_matrix(matrix, 1, buff, width)
        bfill_matrix(matrix, 2, buff, width)

        if len(buff) < args.size:
            break

    print_matrix(matrix)

    # Volcamos a disco lo procesado
    dump_matrix(rot_fd, matrix)

    exit(0)
