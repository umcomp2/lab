#!/usr/bin/python3
import os
import argparse
from manager import open_file, header, rotate_header, write_in_ppm, plain_matrix
from threading import Thread, Barrier

barrier = Barrier(4)
# j indica la posicion dentro del pixel
def rotate(chunk, chunksz, j, sentido):

    # empty es una variable global que representa a la nueva imagen
    global empty

    if sentido == 'r':
        # fila inicial en empty
        f = 0
        # columna inicial en empty
        c = len(empty[0])-1
        b = 0
        index = [f, c ,b]
        # cantidad de filas de la nueva matriz rotada
        rows = len(empty)
        total = 0
        while True:
            # realiza un wait para no empezar a ejecutar antes de que 
            # el hilo main haya llenado el buffer
            barrier.wait()

            # a cada byte lo reubicamos en la nueva matriz
            # chunk[0] es el buffer
            for i in chunk[0][j::3]:
                # le indicamos el indice
                empty[index[0]][index[1]][j] = i
                # subimos una fila
                index[0] += 1
                total += 1
                # aca hace el ultimo ingreso a la matriz rotada
                # if index[0] == -1 and index[1] == rows+1:
                #     empty[index[0]][index[1]][j] = i
                #     total += 1
                # cuando se ingresaron todos los elementos de una columnna, pasamos a la siguiente
                if index[0] == rows:
                    index[0] = 0
                    index[1] -= 1
            # condicion para que frene el loop
            # cuando no haya nada mas para leer
            if len(chunk[0]) < chunksz :
                break
            barrier.wait()  


    if sentido == 'l':
        # fila inicial en empty
        f = len(empty) - 1
        # columna inicial en empty
        c = 0
        b = 0
        index = [f, c ,b]
        # cantidad de filas de la nueva matriz rotada
        rows = len(empty)
        total = 0
        while True:
            # realiza un wait para no empezar a ejecutar antes de que 
            # el hilo main haya llenado el buffer
            barrier.wait()
            # a cada byte lo reubicamos en la nueva matriz
            # chunk[0] es el buffer
            for i in chunk[0][j::3]:
                # le indicamos el indice
                empty[index[0]][index[1]][j] = i
                # subimos una fila
                index[0] -= 1
                total += 1
                # cuando se ingresaron todos los elementos de una columnna, pasamos a la siguiente
                if index[0] == -1:
                    index[1] += 1
                    index[0] = rows - 1
            # condicion para que frene el loop
            # cuando no haya nada mas para leer
            if len(chunk[0]) < chunksz :
                print(empty)
                break
            barrier.wait()  

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='TP1 - procesa ppm')
    parser.add_argument('-s', '--size', action="store", metavar='SIZE', type=int,
                        required=True, help='Bloque de lectura')
    parser.add_argument('-f', '--file', action="store", metavar='FILE', type=str,
                        required=True, help='archivo a procesar')
    parser.add_argument('-d', '--direccion', action="store", metavar='SIZE', type=str,
                        required=True, help='Sentido de la rotacion')
    
    args = parser.parse_args()
    fd = args.file
    # chequeamos que se multiplo de 3
    chunk = args.size - (args.size%3) 
    sentido = args.direccion
    # abrimos le archivo
    file = open_file(fd)
    head, length = header(file) 
    len_head = length
    rotated_content_header, inverted_sz, o_size = rotate_header(head)
    os.lseek(file, len_head, 0)
    # es la matriz vacia pero rotada
    empty = plain_matrix(o_size)
    new = [0]
    threads = []
    for i in range(3):
        # agregamos hilos a la lista thread
        threads.append(Thread(target=rotate, args=(new, chunk, i, sentido)))
    contador = 0
    # el tamaño de la imagen rotada
    total_size = len(empty)* (len(empty[0])) * (len(empty[0][0]))
    while True:
        text = os.read(file, chunk)
        new[0] = text
        # para que no joda el ultimo salto
        if len(new[0]) % 3 != 0:
            new[0] = new[0][:-1]
        # suma lo leido
        contador += len(new[0])
        # solo startea hilos si no fueron starteados anteriormente
        for i in threads:
            if i.is_alive() == False:
                i.start()
        # hacamos un wait para que no se ejecuten los threads primero
        barrier.wait()
        # corta cuando el largo de lo leido sea menor al 
        # tamaño del chunk y cuanodo el contador sea igual
        # al tamaño total
        if len(text) < chunk and contador == total_size :
            break    
        # que no se ejecuten los hilos cuando no hay nada nuevo en el buffer
        barrier.wait()
    for i in threads:
        i.join()
    # lo escribimos en la imagen nueva
    write_in_ppm(empty, rotated_content_header, fd, sentido)
    os.close(file)
    print('\nse rotó correctamente la imagen')
