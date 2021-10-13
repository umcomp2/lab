
import threading
import argparse_1
import os
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor

global_path = argparse_1.path

fd = os.open(global_path, os.O_RDONLY)

rotada = []

def get_header():
    header = []
    fd = os.open(global_path, os.O_RDONLY)
    data = os.read(fd, 100)
    values = data.split()
    dimension_pixeles = []
    try:
        for i in values:
            i.decode()
            if len(dimension_pixeles) < 2:
                if i.isdigit():
                    dimension_pixeles.append(i)
            if len(header) <= 3:
                if i.isdigit() or i == b'P6':
                    header.append(i)
            else:
                break
    except UnicodeDecodeError:
        pass

    bytes_ruster = (int(header[1])*int(header[2]))*3
    bytes_archivo = os.stat(global_path).st_size
    bytes_header = (bytes_archivo-bytes_ruster)

    return header, bytes_header, bytes_ruster, bytes_archivo, dimension_pixeles


def ruster(header, bytes_ruster, n, filas_ruster, columnas_ruster):

    contador = 0  # posicion en ruster
    pixel = []
    pixeles = 0
    pixeles_totales = filas_ruster*columnas_ruster
    red = []
    green = []
    blue = []

    if global_path == 'yacht.ppm':
        header = header
    else:
        header -= 1

    os.lseek(fd, header, 0)  # puntero en ruster

    while pixeles != pixeles_totales:
        leido = os.read(fd, n)
        for i in leido:
            fila = int(pixeles/(columnas_ruster))
            columna = pixeles - (fila * (columnas_ruster))
            if contador % 3 == 0:
                red.append([i, columnas_ruster-columna-1, fila,0])
            elif contador % 3 == 1:
                green.append([i, columnas_ruster-columna-1, fila,1])
            elif contador % 3 == 2:
                blue.append([i, columnas_ruster-columna-1, fila,2])
            pixel.append(i)
            if len(pixel) == 3:
                pixeles += 1
                pixel.clear()
            contador += 1

    if global_path != 'yacht.ppm':
        red.pop()
    return red, green, blue


def matriz_plantilla_izq(filas, columnas):
    global rotada
    for i in range(columnas):
        rotada.append([])
        for j in range(filas):
            rotada[i].append(['R', 'G', 'B'])

    return rotada


def llenar_matriz(i):
    global rotada
    lock.acquire()
    rotada[i[1]][i[2]][i[3]] = i[0]
    lock.release()


def lista(lista_header, rotada):
    fd2 = os.open('rotado7.ppm', os.O_RDWR | os.O_CREAT)
    # roto alto x ancho
    lista_header_rotada = [lista_header[0],
                           lista_header[2], lista_header[1], lista_header[3]]

    for i in lista_header_rotada:
        os.write(fd2, bytes(i))
        os.write(fd2, b'\n')

    lista = []

    for i in rotada:
        for j in i:
            for k in j:
                lista.append(int(k))

    for i in lista:
        os.write(fd2, i.to_bytes(1, byteorder="big"))


if __name__ == '__main__':

    lista_header, bytes_header, bytes_ruster, bytes_archivo, dimension_pixeles = get_header()
    filas_ruster = int(dimension_pixeles[1])
    columnas_ruster = int(dimension_pixeles[0])
    print('ruster sin rotacion de {} x {}'.format(filas_ruster, columnas_ruster))
    lista_red, lista_green, lista_blue = ruster(bytes_header, bytes_ruster, argparse_1.numero, filas_ruster, columnas_ruster)
    rotada = matriz_plantilla_izq(filas_ruster, columnas_ruster)
    print('ruster rotado de {} x {}'.format(len(rotada), len(rotada[0])))

    #for red, green, blue in zip(lista_red, lista_blue, lista_green):
     #   llenar_matriz(red)
      #  llenar_matriz(green)
       # llenar_matriz(blue)

    lock = Lock()

    with ThreadPoolExecutor(max_workers=3) as executor: 
        executor.map(llenar_matriz, lista_red)
        executor.map(llenar_matriz, lista_green)
        executor.map(llenar_matriz, lista_blue)
    lista(lista_header, rotada)

    print(global_path, ' rotada!')
