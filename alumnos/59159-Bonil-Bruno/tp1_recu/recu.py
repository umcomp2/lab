#!/usr/bin/python3
import argparse
from multiprocessing import Pipe, Process
import os
from posix import O_RDONLY


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
    return [len_header, header]

def escalar(b, scale):
    b = int.from_bytes(b, 'big')
    b = b * scale
    b = b.__round__()
    if b > 255:
        b = 255
    b = b.to_bytes(1, 'big')
    return b

def filter_gen(header, name, color, scale, size, conn):
    name = color + name
    fd = os.open(name, os.O_RDWR | os.O_CREAT)
    os.write(fd, header)
    while True:
        chunk = conn.recv()
        if color == 'r_':
            lista_chunk = []
            for i in chunk:
                lista_chunk.append(bytes([i]))
            for i in range(0, len(lista_chunk)-1, 3):
                lista_chunk[i] = escalar(lista_chunk[i], scale)
                lista_chunk[i+1] = b'\x00'
                lista_chunk[i+2] = b'\x00'
            for i in lista_chunk:
                os.write(fd, i)
        
        if color == 'g_':
            lista_chunk = []
            for i in chunk:
                lista_chunk.append(bytes([i]))
            for i in range(1, len(lista_chunk), 3):
                lista_chunk[i-1] = b'\x00'
                lista_chunk[i] = escalar(lista_chunk[i], scale)
                lista_chunk[i+1] = b'\x00'
            for i in lista_chunk:
                os.write(fd, i)

        if color == 'b_':
            lista_chunk = []
            for i in chunk:
                lista_chunk.append(bytes([i]))
            for i in range(2, len(lista_chunk), 3):
                lista_chunk[i-2] = b'\x00'
                lista_chunk[i-1] = b'\x00'
                lista_chunk[i] = escalar(lista_chunk[i], scale)
            for i in lista_chunk:
                os.write(fd, i)
        if b'' in chunk and len(chunk) < size:
            conn.close()
            break


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Procesador de Imagenes')
    parser.add_argument('-r', '--red', help='Escala para rojo', type=float, default=1) 
    parser.add_argument('-g', '--green', help='Escala para verde', type=float, default=1)
    parser.add_argument('-b', '--blue', help='Escala para azul', type=float, default=1)
    parser.add_argument('-f', '--file', help='Archivo que se desea leer', type=str)
    parser.add_argument('-s', '--size', help='Bloque que desea leer', type=int)
    args = parser.parse_args()

    try:
        fd = os.open(args.file, os.O_RDWR)
    except FileNotFoundError:
        print('ERROR: El archivo no existe')
        exit(1)
    lista_header = header(fd)
    
    args.size = args.size - (args.size % 3)
    if args.size <= 0:
        print("El valor size no puede ser negativo o cero")
        exit(1)


    parent_pipe = []
    child_pipe = []
    for _ in range(3):
        p, h = Pipe()
        parent_pipe.append(p)
        child_pipe.append(h)

    color = ['r_', 'g_', 'b_']
    scale_val = [args.red, args.green, args.blue]
    process = []
    for i in range(3):
        p = Process(target=filter_gen, args=(lista_header[1], args.file, color[i], scale_val[i], args.size, child_pipe[i]))
        process.append(p)
    
    for i in process:
        i.start()

    os.lseek(fd, lista_header[0], 0)
    while True:
        lectura = os.read(fd, args.size)
        for i in parent_pipe:
            i.send(lectura)

        if b'' in lectura and len(lectura) < args.size:
            break
    os.close(fd)
    for i in process:
        i.join()
    
    for i in parent_pipe:
        i.close()

    print('Se crearon los archivos de manera exitosa')
