#!/usr/bin/env python3
import argparse
from threading import Thread, Barrier
import os
import re
import mmap


class HiloDeColor(Thread):
    def __init__(self, color, width, high, matrix, buffer_de_lectura, barrier, size):
        Thread.__init__(self)
        self.color = color
        self.index = 0
        self.width = width
        self.high = high
        self.matrix = matrix
        self.buffer_de_lectura = buffer_de_lectura
        self.barrier = barrier
        self.size = size

    def run(self):
        while True:
            # Esperar que el buffer_de_lecturaer tenga nuevo contenido
            self.barrier.wait()

            self.rotar()

            # verificar tampaño para terminar las iteraciones
            if len(self.buffer_de_lectura[0]) < self.size:
                break

            # Esperar a que todos terminen de leer
            self.barrier.wait()

    def rotar(self):
        for i in range(self.color, len(self.buffer_de_lectura[0]), 3):
            col = int(self.index/self.width)
            row = self.width - self.index % self.width - 1
            self.matrix[row][col][self.color] = self.buffer_de_lectura[0][i]
            self.index += 1


def abrir_imagen(path):
    try:
        fd = os.open(f'{path}', os.O_RDWR)
    except Exception as e:
        print(f'Error {e}')
    return fd

def encontrar_cursor_y_header(m_space):
    cursor = 0
    header = ''
    regex = r"(#.*\n)*(P6|P3)(\n|\s){0,2}(#.*\n)*(\d+)(\n|\s){0,2}(#.*\n)*(\d+)(\n|\s){0,2}(#.*\n)*(255|1023)(\n|\s){0,2}(#.*\n)*"
    while not re.match(regex, header, re.MULTILINE):
        try:
            header += str(m_space.readline(), encoding='utf-8')
            cursor = m_space.tell()
        except Exception as e:
            print(f'Error {e}')
    return cursor, header

def crear_imagen_en_disco(name):
    try:
        fd_img = os.open(f'r_{name}', os.O_CREAT | os.O_RDWR)
    except Exception as e:
        print(f'Error {e}')
    return fd_img

def crear_nuevo_header(header, fd_img):
    regex = r'(#.*\n)*(P6|P3)(\n|\s){0,2}(#.*\n)*(\d+)(\n|\s){0,2}(#.*\n)*(\d+)(\n|\s){0,2}'
    header_cortado = re.search(regex, header)[0]
    header_dividido = re.split('\n| ', header_cortado)
    new_wide, new_high = int(header_dividido[-3]), int(header_dividido[-2])
    new_header = f'P6\n{new_high} {new_wide}\n255\n'
    os.write(fd_img, bytes(new_header, 'utf-8'))
    return new_header, new_high, new_wide,

def crear_matriz_rotada(new_high, new_wide):
    matrix = [[[0, 0, 0] for i in range(new_high)] for j in range(new_wide)]
    return matrix

def guarda_matriz_en_disco(fd, matrix):
    for i in matrix:
        buffer_de_lectura = b''
        for j in i:
            buffer_de_lectura += bytes([j[0], j[1], j[2]])
        os.write(fd, buffer_de_lectura)

def parser_image():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Archivo a procesar',
                        required=True)
    parser.add_argument('-n', '--valor', help='Bloque de lectura', type=int,
                        required=True)
    return parser.parse_args()

def validar_bloque_de_lectura(bloque_de_lectura):
    if bloque_de_lectura < 3:
        bloque_de_lectura = 3
    else:
        bloque_de_lectura = bloque_de_lectura - bloque_de_lectura % 3
    return bloque_de_lectura

def crear_lista_de_hilos(width, high, matrix, buffer_de_lectura, barrier_sincro, bloque_de_lectura):
    lista_de_hilos = list()
    for i in range(3):
        try:
            hilo_de_color = HiloDeColor(i, width, high, matrix, buffer_de_lectura, barrier_sincro, bloque_de_lectura)
            lista_de_hilos.append(hilo_de_color)
        except Exception as e:
            print(f'Error {e} al crear lista_de_hilos')
            for i in fd_list:
                os.close(i)
    return lista_de_hilos

def leer_x_bloques(fd, bloque_de_lectura, bytes_leidos, barrier_sincro, ruster):
    while True:
        bloque = os.read(fd, bloque_de_lectura)
        buffer_de_lectura[0] = bloque
        bytes_leidos += len(bloque)

        # Comprobar el caso que termine con \n
        if len(buffer_de_lectura[0]) % 3 != 0:
            buffer_de_lectura[0] = buffer_de_lectura[0][:-1]

        # esperar que se cargue el buffer_de_lectura
        barrier_sincro.wait()

        if len(buffer_de_lectura[0]) < bloque_de_lectura and bytes_leidos >= ruster:
            break

        # esperar que todos terminen de leer
        barrier_sincro.wait()

def iniciar_hilos(lista_de_hilos):
    for i in lista_de_hilos:
        i.start()

def esperar_hilos(lista_de_hilos):
    for i in lista_de_hilos:
        i.join()

def cerrar_fds(fd_list):
    for i in fd_list:
        os.close(i)


if __name__ == "__main__":
    args = parser_image()
    nombre_archivo = args.file
    bloque_de_lectura = args.valor
    bloque_de_lectura = validar_bloque_de_lectura(bloque_de_lectura)

    # Lista de fd para cerrarlos mas facil
    fd_list = list()
    fd = abrir_imagen(f'{nombre_archivo}')
    fd_list.append(fd)

    # Mapear imagen a memoria
    m_img = mmap.mmap(fd, 0)
    inicio_pl, header = encontrar_cursor_y_header(m_img)
    m_img.close()

    # Crear el archivo donde se va a volcar y la matriz transpuesta
    rot_fd = crear_imagen_en_disco(nombre_archivo)
    start, high, width = crear_nuevo_header(header, rot_fd)
    matrix = crear_matriz_rotada(high, width)
    fd_list.append(rot_fd)

    # Pararnos en el comienzo del ruster
    os.lseek(fd, inicio_pl, 0)

    buffer_de_lectura = list(b'\x00')
    barrier_sincro = Barrier(4)
    lista_de_hilos = crear_lista_de_hilos(width, high, matrix, buffer_de_lectura, barrier_sincro, bloque_de_lectura)

    # Variables de control
    ruster = width*high*3
    bytes_leidos = 0

    iniciar_hilos(lista_de_hilos)

    leer_x_bloques(fd, bloque_de_lectura, bytes_leidos, barrier_sincro, ruster)
    esperar_hilos(lista_de_hilos)

    guarda_matriz_en_disco(rot_fd, matrix)

    cerrar_fds(fd_list)

    print("Imagen rotada con exito!")
