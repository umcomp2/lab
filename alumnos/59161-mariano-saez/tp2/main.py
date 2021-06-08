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

    # Crear y [volcar ruster]
    matrix = [[[0, 0, 0] for i in range(new_wide)] for j in range(new_high)]
    chorizo = b''
    for i in range(new_high):
        for j in range(new_wide):
            for k in matrix[i][j]:
                chorizo += k
    os.write(fd_img, chorizo)

    return fd_img, len(new_header)

def rotate(high=256, wide=256):
    # Matriz de elementos que representan la imagen
    matrix = [[b'\xff', b'\xff', b'\xff'] for i in range(high*wide)]



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

    # Se abre el archivo con manejo de errores
    fd = open_image(f'{args.file}')

    # Mapear imagen a memoria, posicionarse en el payload y obtener
    # el header
    m_img = mmap.mmap(fd, 0)
    inicio_pl, header = seek_payload(m_img)
    m_img.close()

    rot_fd, start = gen_file(header, args.file)
    # rotate()


