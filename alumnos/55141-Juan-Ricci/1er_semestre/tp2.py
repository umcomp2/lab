import argparse as ap
import os
from concurrent.futures import ThreadPoolExecutor
import threading
from tp2_copiado import header_size
from matriz import inicializar_matriz
from manejar_header import quitar_header, ppm_size
import logging

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

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
    if color == 'r':
        for i in range(0,len(chunk)-1,3):
            matriz[fila_r][columna_r][0] = chunk[i]
            fila_r-=1
            if fila_r == -1:
                fila_r = height -1 
                columna_r += 1
    
    if color == 'g':
        for i in range(1,len(chunk),3):
            matriz[fila_g][columna_g][1] = chunk[i]
            fila_g-=1
            if fila_g == -1:
                fila_g = height -1 
                columna_g += 1

    if color == 'b':        
        for i in range(2,len(chunk),3):
            matriz[fila_b][columna_b][2] = chunk[i]
            fila_b-=1
            if fila_b == -1:
                fila_b = height -1 
                columna_b += 1


if __name__ == '__main__':

    parser = ap.ArgumentParser()
    parser.add_argument('-f', '--file', action='store', type=str, help='Archivo a rotar', required=True)
    parser.add_argument('-s', '--size', action='store', type=int, help='Tamano del bloque a leer')
    args = parser.parse_args()

    chunk_sz = multiplo3(args.size)

    fd = open(f'{args.file}', 'rb')
    leido = fd.read()
    cuerpo, tipo, w_and_h, prof, header = quitar_header(leido)
    width, height = ppm_size(w_and_h)

    new_width = int(height)
    new_height = int(width)
    
    if os.path.isfile(f'{args.file}'.replace('.ppm','_rotado.ppm')):
        os.remove(f'{args.file}'.replace('.ppm','_rotado.ppm'))
    ppm_rotado = open(f'{args.file}'.replace('.ppm','_rotado.ppm'), 'a')
    ppm_rotado.write(f'{tipo.decode("utf-8")}\n{new_width} {new_height}\n{int(prof)}\n')

    columna_r = 0
    columna_g = 0
    columna_b = 0
    fila_r = new_height - 1
    fila_g = new_height - 1
    fila_b = new_height - 1

    matriz = inicializar_matriz(new_width, new_height)
    #print(matriz)

    #threads = []

    executor = ThreadPoolExecutor(max_workers=3)

    colores = ['r', 'g', 'b']
    '''for color in colores:
        rotar(new_height,color,cuerpo)'''
    for i in range(0, len(cuerpo), chunk_sz):
        chunk = cuerpo[i:i + chunk_sz]
        for color in colores:
            rotar(new_height,color,chunk)
            #t = executor.submit(rotar(new_height, color, chunk))
            #t = threading.Thread(target=rotar, args=(new_height, color, chunk,))
            #t.start()
            #threads.append(t)
        
    '''for t in threads:
        t.join()'''

    #imagen_rotada = open(f'{args.file}'.replace('.ppm','_rotado.ppm'), 'a') 

    for i in matriz:
        for j in i:
            for k in j:
                ppm_rotado.write(chr(k))

    #print(threads)
    fd.close()
    ppm_rotado.close()
    #print(matriz)

