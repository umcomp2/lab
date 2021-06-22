#!/usr/bin/python3
import argparse
import os
from posix import O_RDONLY
from threading import Barrier, Thread

def new_header(header):
    header = header.split(b'\n')
    if b'#' in header[1]:
        dim = header[2].split(b' ')
        dim[0], dim[1] = dim[1], dim[0]
        width = int(dim[0].decode('utf-8'))
        height = int(dim[1].decode('utf-8'))
        dim = b' '.join(dim)
        header[2] = dim
        header = b'\n'.join(header)
    else:
        dim = header[1].split(b' ')
        dim[0], dim[1] = dim[1], dim[0]
        width = int(dim[0].decode('utf-8'))
        height = int(dim[1].decode('utf-8'))
        dim = b' '.join(dim)
        header[1] = dim
        header = b'\n'.join(header)
    return [header, width, height]


def header(fd):
    leer_header = os.read(fd, 50)
    leer_header = (leer_header.split(b'\n'))
    len_header = 0
    for i in range(len(leer_header)):
        if leer_header[i-1] == b'255':
            break
        len_header += (len(leer_header[i]))
        len_header += 1
    os.lseek(fd, 0, 0)
    header = os.read(fd, len_header)
    return header


def rotar(h, color):
    global matriz
    global lectura
    block = list()
    while True:
        b.wait()
        for i in lectura:
            block.append(bytes([i]))

        f = h
        c = 0
        for i in block[color::3]:
            if f == 0:
                c += 1
                f = h
            matriz[f-1][c][color] = i
            f -= 1

        if len(lectura) < args.size:
            break
        b.wait()

def escribir(file):
    global matriz
    for i in matriz:
        b = b''
        for j in i:
            b += b''.join(j)
        os.write(file, b)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Procesador de Imagenes')
    parser.add_argument('-f', '--file', help='Archivo que se desea leer', type=str)
    parser.add_argument('-s', '--size', help='Bloque que desea leer', type=int)
    args = parser.parse_args()

    file = args.file

    b = Barrier(4)

    try:
        fd = os.open(file, os.O_RDWR)
    except FileNotFoundError:
        print('ERROR: El archivo no existe')
        exit(1)


    hd = header(fd)
    header_ls = new_header(hd)
    long = len(header_ls[0])

    name = 'left_' + file
    new_file = os.open(name, os.O_CREAT | os.O_RDWR)
    os.write(new_file, header_ls[0])

    matriz = [[[0,0,0] for i in range(header_ls[1])] for i in range(header_ls[2])]
    lectura = b''

    color = [0, 1, 2]
    
    hilos = list()
    for i in range(3):
        t = Thread(target=rotar, args=(header_ls[2], color[i]))
        hilos.append(t)


    args.size = args.size - (args.size % 3)
    if args.size <= 0:
       print("El valor size no puede ser negativo o cero")
       exit(1)


    os.lseek(fd, long, 0)
    while True:
        lectura = os.read(fd, args.size)
        if len(lectura) % 3 != 0:
            lectura = lectura[:-1]
        for i in hilos:
            if i.is_alive() == False:
                i.start()
        b.wait()
        if len(lectura) < args.size:
            break
        b.wait()

    for i in hilos:
        i.join()

    escribir(new_file)
    print('La imagen se roto correctamente')
    
