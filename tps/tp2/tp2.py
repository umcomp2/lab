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

def rotar_izquierda(height, color, chunk):
    global columna_r
    global fila_r
    global columna_g
    global fila_g
    global columna_b
    global fila_b
    global matriz
    global pixeles
    global threadLock
    if color == 'r':
        #threadLock.acquire()
        for i in range(0,len(chunk)-1,3):
            matriz[fila_r][columna_r][0] = pixeles[i] #chr(chunk[i]).encode("utf-8")
            fila_r-=1
            if fila_r == -1:
                fila_r = height -1 
                columna_r += 1
        #threadLock.release()
        b.wait()

    if color == 'g':
        #threadLock.acquire()
        for i in range(1,len(chunk),3):
            matriz[fila_g][columna_g][1] = pixeles[i] #chr(chunk[i]).encode("utf-8")
            fila_g-=1
            if fila_g == -1:
                fila_g = height -1 
                columna_g += 1
        #threadLock.release()
        b.wait()

    if color == 'b':  
        #threadLock.acquire()      
        for i in range(2,len(chunk),3):
            matriz[fila_b][columna_b][2] = pixeles[i] #chr(chunk[i]).encode("utf-8")
            fila_b-=1
            if fila_b == -1:
                fila_b = height -1 
                columna_b += 1
        #threadLock.release()
        b.wait()

def rotar_derecha(height, color, chunk):
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
            fila_r += 1
            if fila_r == height:
                fila_r = 0 
                columna_r -= 1
        #threadLock.release()
        b.wait()

    if color == 'g':
        #threadLock.acquire()
        for i in range(1,len(chunk),3):
            matriz[fila_g][columna_g][1] = pixeles[i] #chr(chunk[i]).encode("utf-8")
            fila_g += 1
            if fila_g == height:
                fila_g = 0 
                columna_g -= 1
        #threadLock.release()
        b.wait()

    if color == 'b':  
        #threadLock.acquire()      
        for i in range(2,len(chunk),3):
            matriz[fila_b][columna_b][2] = pixeles[i] #chr(chunk[i]).encode("utf-8")
            fila_b += 1
            if fila_b == height:
                fila_b = 0 
                columna_b -= 1
        #threadLock.release()
        b.wait()

if __name__ == '__main__':

    parser = ap.ArgumentParser("Tp2 - procesa ppm\n\n")
    parser.add_argument('-f', '--file', action='store', type=str, help='Archivo a rotar', required=True)
    parser.add_argument('-s', '--size', action='store', type=int, help='Tamano del bloque a leer')
    parser.add_argument('--sentido', action='store', type=str, default='i', help="Sentido de giro (ingresar d [derecha] o i [izquierda])")
    args = parser.parse_args()

    sentido = args.sentido

    manejo_de_errores(parser, args.file, args.size, sentido)

    chunk_sz = multiplo3(args.size)

    fd = os.open(args.file, os.O_RDONLY)
    header, size = find_header(fd)
    #print(header)

    uncommented_header = uncomment(header)
    #print(uncommented_header)
    
    rotated_header, width, height = rotate_header(uncommented_header)

    rotated_ppm = os.open(f'rotated_{args.file}', os.O_RDWR | os.O_CREAT)
    os.write(rotated_ppm, rotated_header)
    
    '''rotated_ppm = open(f'rotated_file_{args.file}', 'ab')
    rotated_ppm.write(bytes(rotated_header))'''

    os.lseek(fd, size, 0)

    matriz = inicializar_matriz(width, height)

    if sentido == 'i':
        columna_r = 0
        columna_g = 0
        columna_b = 0
        fila_r = height - 1
        fila_g = height - 1
        fila_b = height - 1
    elif sentido == 'd':
        columna_r = width - 1
        columna_g = width - 1
        columna_b = width - 1
        fila_r = 0
        fila_g = 0
        fila_b = 0

    #threadLock = threading.Lock()
    b = threading.Barrier(3)

    threads = []
    '''colores = ['r', 'g', 'b']'''
    
    while True:
        chunk = os.read(fd, chunk_sz)
        pixeles = list()
        for i in chunk:
            pixeles.append(bytes([i]))
        #print(chunk)
        '''with ThreadPoolExecutor(max_workers=3) as executor:
            for color in colores:
                t = executor.submit(rotar(height, color, chunk))'''
        if sentido == 'i':
            t1 = threading.Thread(target=rotar_izquierda, args=(height, 'r', chunk,))
            t2 = threading.Thread(target=rotar_izquierda, args=(height, 'g', chunk,))
            t3 = threading.Thread(target=rotar_izquierda, args=(height, 'b', chunk,))
        elif sentido == 'd':
            t1 = threading.Thread(target=rotar_derecha, args=(height, 'r', chunk,))
            t2 = threading.Thread(target=rotar_derecha, args=(height, 'g', chunk,))
            t3 = threading.Thread(target=rotar_derecha, args=(height, 'b', chunk,))
        t1.start()
        t2.start()
        t3.start()
        threads.append(t1)
        threads.append(t2)
        threads.append(t3)
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

    if sentido == 'i':
        print(f"Se rotó correctamente la imagen hacia la izquierda")
    elif sentido == 'd':
        print(f"Se rotó correctamente la imagen hacia la derecha")