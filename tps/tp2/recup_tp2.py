#!/usr/bin/python3
import os
import argparse as ap
from concurrent.futures import ThreadPoolExecutor
from manejar_header import find_header, uncomment, rotate_header
from matriz import inicializar_matriz
from manejar_errores import manejo_de_errores
import threading


def multiplo3(num):
    aprox=int(num-(num%3))
    return aprox

def espejar(width, color, chunk):
    global columna_r
    global fila_r
    global columna_g
    global fila_g
    global columna_b
    global fila_b
    global matriz
    global pixeles
    if color == 'r':
        #threadLock.acquire()
        for i in range(0,len(chunk)-1,3):
            matriz[fila_r][columna_r][0] = pixeles[i] #chr(chunk[i]).encode("utf-8")
            columna_r -= 1
            if columna_r < 0:
                fila_r += 1 
                columna_r = width - 1
        #threadLock.release()
        #b.wait()

    if color == 'g':
        #threadLock.acquire()
        for i in range(1,len(chunk),3):
            matriz[fila_g][columna_g][1] = pixeles[i] #chr(chunk[i]).encode("utf-8")
            columna_g -= 1
            if columna_g < 0:
                fila_g += 1 
                columna_g = width - 1
        #threadLock.release()
        #b.wait()

    if color == 'b':  
        #threadLock.acquire()      
        for i in range(2,len(chunk),3):
            matriz[fila_b][columna_b][2] = pixeles[i] #chr(chunk[i]).encode("utf-8")
            columna_b -= 1
            if columna_b < 0:
                fila_b += 1 
                columna_b = width - 1
        #threadLock.release()
        #b.wait()

if __name__ == '__main__':

    parser = ap.ArgumentParser("Tp2 - procesa ppm\n\n")
    parser.add_argument('-f', '--file', action='store', type=str, help='Archivo a rotar', required=True)
    parser.add_argument('-s', '--size', action='store', type=int, help='Tamano del bloque a leer')
    args = parser.parse_args()

    manejo_de_errores(parser, args.file, args.size)

    chunk_sz = multiplo3(args.size)

    fd = os.open(args.file, os.O_RDONLY)
    header, size = find_header(fd)
    #print(header)

    uncommented_header = uncomment(header)
    #print(uncommented_header)
    
    rotated_header, width, height = rotate_header(uncommented_header)

    rotated_ppm = os.open(f'mirrored_{args.file}', os.O_RDWR | os.O_CREAT)
    os.write(rotated_ppm, rotated_header)
    
    '''rotated_ppm = open(f'rotated_file_{args.file}', 'ab')
    rotated_ppm.write(bytes(rotated_header))'''

    os.lseek(fd, size, 0)

    matriz = inicializar_matriz(width, height)
    #print(matriz)

    
    columna_r = width - 1
    columna_g = width - 1
    columna_b = width - 1
    fila_r = 0
    fila_g = 0
    fila_b = 0

    #threadLock = threading.Lock()
    b = threading.Barrier(3)

    threads = []
    colores = ['r', 'g', 'b']
    executor = ThreadPoolExecutor(max_workers=3)
    
    while True:
        chunk = os.read(fd, chunk_sz)
        pixeles = list()
        for i in chunk:
            pixeles.append(bytes([i]))
        #print(chunk)
        for color in colores:
                t = executor.submit(espejar(width, color, chunk))
        if len(chunk) < chunk_sz:
            break

    for t in threads:
        t.join()

    #print(matriz)

    for i in matriz:
        for j in i:
            for k in j:
                #rotated_ppm.write(bytes(k))
                os.write(rotated_ppm, bytes(k))

    os.close(fd)
    os.close(rotated_ppm)

    print(f"Se espejó correctamente la imagen")