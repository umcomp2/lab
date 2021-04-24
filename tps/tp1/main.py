#!/usr/bin/env python3
import argparse
from worker import Histogramer
import errores
import os
import sys
import mmap
import multiprocessing as mp
import re

STDIN = 0
STDOUT = 1
STDERR = 2
EOF = b''
CHILDNO = 3
RGB = [0, 1, 2]

# ====================== PPM ANALYZER ======================

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
           for i in pipe_arr:
                i.send(EOF)
           break
    for i in pipe_arr:
        i.close()


if __name__ == "__main__":
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
    args = parser.parse_args()

    # Obtener un file descriptor con manejo de errores
    fd = open_image(f'{args.file}')

    # Mapear imagen a memoria, posicionarse en el payload y obtener
    # el header
    m_img = mmap.mmap(fd, 0)
    inicio_pl, header = seek_payload(m_img)

    # Crear histogramers y pipes para IPC
    pipes_for_parent = list()
    histogramer_list = list()
    for i in range(CHILDNO):
        parent, child = mp.Pipe()
        pipes_for_parent.append(parent)
        histogramer_list.append(Histogramer(RGB[i], child, args.size, args.file, header))

    # Iniciar hijos
    for i in histogramer_list:
        i.start()
    
    # Leer de a chunks (size especificado por argumento)
    read_by_chunks(fd, inicio_pl, args.size, pipes_for_parent)
    
    # Esperar a los hijos
    for i in histogramer_list:
        i.join()

    # Tareas del hogar
    child.close()
    for i in pipes_for_parent:
        i.close()
    m_img.close()
    os.close(fd)

    print('Se generaron correctamente los 3 histogramas')
