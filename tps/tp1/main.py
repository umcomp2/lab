#!/usr/bin/env python3
import argparse
from worker import Histogramer
import errores
import os
import sys
import mmap
import multiprocessing as mp

# TODO: Funciones de procesos hijos
# TODO: RegEx https://regex101.com/r/oOpHlJ/1 (#.*\n)*(P6|P3)(\n|\s){0,2}(#.*\n)*(\d+)(\n|\s){0,2}(#.*\n)*(\d+)(\n|\s){0,2}(#.*\n)*(255|1023)(\n|\s){0,2}(#.*\n)*

# EXTRA: Ver como agregar filtro de color


STDIN = 0
STDOUT = 1
STDERR = 2
EOF = b''
CHILDNO = 3
RGB = [0, 1, 2]


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
        sys.exit()
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
    format_flag = False
    try:
        while True:
            buff = m_space.readline()
            cursor = m_space.tell()
            if b'P6' in buff:
                format_flag = True
            if buff == b'255\n':
                break
        if not format_flag:
            raise errores.FormatIdentifierNotFound
    
    except errores.FormatIdentifierNotFound:
        print(f'El archivo no posee un identificador de formato PPM')
        sys.exit(1)
    

    return cursor


# Funcion encargada de leer por chunks el archivo indicado
#   @fd: File descriptor del archivo a leer
#   @start: Offset donde empezar a leer
#   @chunk_sz: Cantidad de bytes por lectura
#   @pipe_arr: Array de pipes donde escribir
def read_by_chunks(fd: int, start: int, chunk_sz: int, pipe_arr: list):
    os.read(fd, start)
    while True:
        chunk = os.read(fd, chunk_sz)
        for i in pipe_arr:
            i.send(chunk)
        if len(chunk) < chunk_sz:
           print('fin envio')
           for i in pipe_arr:
                i.send(EOF)
           break
    for i in pipe_arr:
        i.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', metavar='FILE',
                        help='Archivo a procesar')
    parser.add_argument('-s', '--size', metavar='SIZE',
                        help='Bloque de lectura', type=int)
    args = parser.parse_args()

    # Obtener un file descriptor con manejo de errores
    fd = open_image(f'{args.file}')

    # Mapear imagen a memoria y posicionarse en el payload
    m_img = mmap.mmap(fd, 0)
    inicio_pl = seek_payload(m_img)

    # Crear histogramers y pipes para IPC
    pipes_for_parent = list()
    histogramer_list = list()
    for i in range(CHILDNO):
        parent, child = mp.Pipe()
        pipes_for_parent.append(parent)
        histogramer_list.append(Histogramer(RGB[i], child, args.size, args.file))

    # TEST: Crear hijo que lee rojo
    for i in histogramer_list:
        i.start()
    
    # Leer de a chunks especificados por argumento
    read_by_chunks(fd, inicio_pl, args.size, pipes_for_parent)
    
    
    for i in histogramer_list:
        i.join()

    print('exito!')


    
    