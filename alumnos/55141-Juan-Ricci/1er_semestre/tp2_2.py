from concurrent import futures
import os
import argparse as ap
from concurrent.futures import ThreadPoolExecutor
from manejar_header import find_header, uncomment, rotate_header
from matriz import inicializar_matriz
import threading


def multiplo3(num):
    aprox=int(num-(num%3))
    return aprox

def rotar(height, color, chunk):
    global columna_r
    global fila_r
    global columna_g
    global fila_g
    global columna_b
    global fila_b
    global matriz
    global pixeles
    if color == 'r':
        threadLock.acquire()
        for i in range(0,len(chunk)-1,3):
            matriz[fila_r][columna_r][0] = pixeles[i] #chr(chunk[i]).encode("utf-8")
            fila_r-=1
            if fila_r == -1:
                fila_r = height -1 
                columna_r += 1
        #print(threading.get_ident())
        threadLock.release()

    if color == 'g':
        threadLock.acquire()
        for i in range(1,len(chunk),3):
            matriz[fila_g][columna_g][1] = pixeles[i] #chr(chunk[i]).encode("utf-8")
            fila_g-=1
            if fila_g == -1:
                fila_g = height -1 
                columna_g += 1
            
        #print(threading.get_ident())
        threadLock.release()

    if color == 'b':  
        threadLock.acquire()      
        for i in range(2,len(chunk),3):
            matriz[fila_b][columna_b][2] = pixeles[i] #chr(chunk[i]).encode("utf-8")
            fila_b-=1
            if fila_b == -1:
                fila_b = height -1 
                columna_b += 1
            
        #print(threading.get_ident())
        threadLock.release()

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
        threadLock.acquire()
        for i in range(0,len(chunk)-1,3):
            matriz[fila_r][columna_r][0] = pixeles[i] #chr(chunk[i]).encode("utf-8")
            fila_r += 1
            if fila_r == height:
                fila_r = 0 
                columna_r -= 1
        #print(threading.get_ident())
        threadLock.release()

    if color == 'g':
        threadLock.acquire()
        for i in range(1,len(chunk),3):
            matriz[fila_g][columna_g][1] = pixeles[i] #chr(chunk[i]).encode("utf-8")
            fila_g += 1
            if fila_g == height:
                fila_g = 0 
                columna_g -= 1
            
        #print(threading.get_ident())
        threadLock.release()

    if color == 'b':  
        threadLock.acquire()      
        for i in range(2,len(chunk),3):
            matriz[fila_b][columna_b][2] = pixeles[i] #chr(chunk[i]).encode("utf-8")
            fila_b += 1
            if fila_b == height:
                fila_b = 0 
                columna_b -= 1
            
        #print(threading.get_ident())
        threadLock.release()

if __name__ == '__main__':

    parser = ap.ArgumentParser()
    parser.add_argument('-f', '--file', action='store', type=str, help='Archivo a rotar', required=True)
    parser.add_argument('-s', '--size', action='store', type=int, help='Tamano del bloque a leer')
    args = parser.parse_args()

    chunk_sz = multiplo3(args.size)

    fd = os.open(args.file, os.O_RDONLY)
    header, size = find_header(fd)
    #print(header)

    uncommented_header = uncomment(header)
    #print(uncommented_header)
    
    rotated_header, width, height = rotate_header(uncommented_header)

    rotated_ppm = os.open(f'rotated_file_{args.file}', os.O_RDWR | os.O_CREAT)
    os.write(rotated_ppm, rotated_header)
    
    '''rotated_ppm = open(f'rotated_file_{args.file}', 'ab')
    rotated_ppm.write(bytes(rotated_header))'''

    os.lseek(fd, size, 0)

    matriz = inicializar_matriz(width, height)

    '''columna_r = 0
    columna_g = 0
    columna_b = 0
    fila_r = height - 1
    fila_g = height - 1
    fila_b = height - 1'''
    columna_r = width - 1
    columna_g = width - 1
    columna_b = width - 1
    fila_r = 0
    fila_g = 0
    fila_b = 0

    threadLock = threading.Lock()

    threads = []
    
    while True:
        chunk = os.read(fd, chunk_sz)
        pixeles = list()
        for i in chunk:
            pixeles.append(bytes([i]))
        #print(chunk)
        #print(pixeles)
        '''t1 = threading.Thread(target=rotar, args=(height, 'r', chunk,))
        t2 = threading.Thread(target=rotar, args=(height, 'g', chunk,))
        t3 = threading.Thread(target=rotar, args=(height, 'b', chunk,))'''
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
    
    archivo = open("matriz_incorrecta.txt", 'w')
    archivo.write(str(matriz))