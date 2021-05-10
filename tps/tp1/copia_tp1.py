#!/usr/bin/python3
import argparse
import multiprocessing
import os
import matplotlib.pyplot as plt
from itertools import islice
from shutil import copyfile

def read_and_dump(pipe, filename, chunk_sz, color, rojo, verde, azul):
    #fd = os.open(f'{filename}_{color}.txt', os.O_RDWR | os.O_CREAT)
    '''rojo = list()
    verde = list()
    azul = list()'''
    while True:
        chunk = pipe.recv()
        listado = list(islice(chunk, 3)) # divide el chunk cada 3 bytes
        rojo.append(listado[0])
        verde.append(listado[1])
        azul.append(listado[2])
        if len(chunk) < chunk_sz:
            break
    pipe.close()
    return rojo, verde, azul

def crear_hist(pipe, filename, chunk_sz, color, rojo, verde, azul):
    h_r, h_v, h_a = read_and_dump(pipe, filename, chunk_sz, color, rojo, verde, azul)
    plt.hist(h_r, bins=256, color = 'red', edgecolor='red')
    plt.savefig('red.png')
    plt.cla()
    plt.hist(h_v, bins=256, color = 'green', edgecolor='green')
    plt.savefig('green.png')
    plt.cla()
    plt.hist(h_a, bins=256, color = 'blue', edgecolor='blue')
    plt.savefig('blue.png')
    plt.cla()

def quitar_header(leido):
    # quito los comentarios
    for i in range(leido.count(b"\n# ")):
        barra_n_as = leido.find(b"\n# ")
        barra_n = leido.find(b"\n", barra_n_as + 1)
        leido = leido.replace(leido[barra_n_as:barra_n], b"")

        # sacar encabezado
    primer_n = leido.find(b"\n") + 1
    seg_n = leido.find(b"\n", primer_n) + 1
    ultima_barra_n = leido.find(b"\n", seg_n) + 1
    encabezado = leido[:ultima_barra_n].decode()

        # guardo el cuerpo
    cuerpo = leido[ultima_barra_n:]
    new_file = open(f'{args.file}_copy', 'wb')
    new_file.write(cuerpo)
    new_file.close()
    fd.close()
    #print(cuerpo)

if __name__ == '__main__':

    # creo los argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', action='store', help='archivo')
    parser.add_argument('-n', type=int, help='Tamano del bloque')
    args = parser.parse_args()
    print (args)

    # creo una copia del archivo a la cual le voy a quitar el header para no modificar el archivo original
    copyfile(args.file, f'{args.file}_copy')

    #fd = os.open(f'{args.file}', os.O_RDWR)
    fd = open(f'{args.file}', 'rb')
    chunk_sz = int(args.n)

    # leo el archivo completo
    leido = fd.read()
    quitar_header(leido)
    
    # creo los ipc
    pipes = []
    procesos = []
    colores = ['red','green','blue']
    rojo = list()
    verde = list()
    azul = list()
    for color in colores: # esto es para que se cree un hijo por cada color (3 hijos)
        parent_pipe, child_pipe = multiprocessing.Pipe()
        pipes.append(parent_pipe)
        p = multiprocessing.Process(target=crear_hist, args=(child_pipe, args.file, chunk_sz, color, rojo, verde, azul) )
        p.start() # inicializo el hijo
        procesos.append(p)

    # leer archivo y escribir al pipe de a chunks
    new_file = open(f'{args.file}_copy', 'rb') 
    while True:
        #chunk = os.read(cuerpo, chunk_sz)
        #chunk = fd.read(chunk_sz)
        chunk = new_file.read(chunk_sz)
        for i in pipes:
            i.send(chunk)
        if len(chunk) < chunk_sz:
            break


    # esperamos a que terminen los hijos
    for i in procesos:
        i.join()

    # cerramos todo
    #os.close(fd)
    #fd.close()
    new_file.close()
    child_pipe.close()
    for i in pipes:
        i.close()