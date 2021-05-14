#!/usr/bin/python3
import argparse
import multiprocessing
#import os
#import matplotlib.pyplot as plt
from itertools import islice
from collections import Counter
import os.path


def read_and_dump(pipe, filename, chunk_sz, color, rojo, verde, azul):
    while True:
        chunk = pipe.recv() # recive el chunk que envie
        listado = list(islice(chunk, 3)) # divide el chunk cada 3 bytes
        rojo.append(listado[0]) # agrego el primer item de la lista a la lista rojo
        verde.append(listado[1]) # agrego el segundo item de la lista a la lista verde
        azul.append(listado[2]) # agrego el tercer item de la lista a la lista azul
        if len(chunk) < chunk_sz:
            break
    pipe.close()
    return rojo, verde, azul

def crear_filtros(pipe, filename, chunk_sz, color, rojo, verde, azul, escala_rojo, escala_verde, escala_azul):
    rojo, verde, azul = read_and_dump(pipe, filename, chunk_sz, color, rojo, verde, azul) # tomo las listas rojo, verde y azul
    if color == 'red':
        filtro_rojo = open(f'r_{filename}', 'w') # creo el archivo para guardar el filtro de rojos
        lista_rojo = list()
        for i in rojo: 
            lista_rojo.append(i) # cada valor del color rojo lo guardo en una sola lista
        lista_rojo.sort() # ordeno la lista
        f_rojo = Counter(lista_rojo) # relizo un conteo de cada item y lo guardo pero me lo vuelve a desordenar (se guarda como tuplas)
        rojo_ordenado = sorted(f_rojo.items()) # ordeno la lista que me devolvio la funcion Counter    
        for tupla in rojo_ordenado:
            lista = list(tupla) # las tuplas son inmutables por lo que debo convertir c/u en una lista,
            lista[1] = lista[1] * escala_rojo # cambiar el valor necesitado
            tupla = tuple(lista) # y volverla a convertir en tupla
            filtro_rojo.write(str(tupla) + '\n') # escribo el resultado en el archivo que cree anteriormente
    
    elif color == 'green':
        filtro_verde = open(f'g_{filename}', 'w')
        lista_verde = list()
        for i in verde:
            lista_verde.append(i)
        lista_verde.sort()
        f_verde = Counter(lista_verde)
        verde_ordenado = sorted(f_verde.items())
        for tupla in verde_ordenado:
            lista = list(tupla)
            lista[1] = lista[1] * escala_verde
            tupla = tuple(lista)
            filtro_verde.write(str(tupla) + '\n')

    elif color == 'blue':
        filtro_azul = open(f'b_{filename}', 'w')
        lista_azul = list()
        for i in azul:
            lista_azul.append(i)
        lista_azul.sort()
        f_azul = Counter(lista_azul)
        azul_ordenado = sorted(f_azul.items())
        for tupla in azul_ordenado:
            lista = list(tupla)
            lista[1] = lista[1] * escala_azul
            tupla = tuple(lista)
            filtro_azul.write(str(tupla) + '\n')

'''def crear_hist(pipe, filename, chunk_sz, color, rojo, verde, azul):
    h_r, h_v, h_a = read_and_dump(pipe, filename, chunk_sz, color, rojo, verde, azul)
    plt.hist(h_r, bins=256, color = 'red', edgecolor='red')
    plt.savefig('red.png')
    plt.cla()
    plt.hist(h_v, bins=256, color = 'green', edgecolor='green')
    plt.savefig('green.png')
    plt.cla()
    plt.hist(h_a, bins=256, color = 'blue', edgecolor='blue')
    plt.savefig('blue.png')
    plt.cla()'''

def quitar_header(leido):
    # quito los comentarios
    for i in range(leido.count(b"\n# ")):
        comienzo_comentario = leido.find(b"\n# ") # busca la posicion del primer \n# 
        sgte_enter = leido.find(b"\n", comienzo_comentario + 1) # busca la posicion del primer \n que le sigue al encontrado anteriormente
        leido = leido.replace(leido[comienzo_comentario:sgte_enter], b"") # reemplaza por un byte vacio todo lo que este entre la posicion del comienzo del comentario y la del \n que le sigue

    # sacar encabezado
    primer_enter = leido.find(b"\n") + 1 # busca la posicion del primer \n
    segundo_enter = leido.find(b"\n", primer_enter) + 1 # busca la posicion del \n que le sigue al anterior
    ultimo_enter = leido.find(b"\n", segundo_enter) + 1 # busca la posicion del siguiente \n que sera el ultimo del encabezado
    #encabezado = leido[:ultimo_enter].decode()  # guarda todo lo que esta antes del ultimo enter

    # guardo el cuerpo
    cuerpo = leido[ultimo_enter:] # guarda todo lo que esta despues del ultimo enter
    new_file = open(f'{args.file}_copy', 'wb')
    new_file.write(cuerpo)
    new_file.close()
    fd.close()
    return cuerpo

def manejo_de_errores(parser, filename, size, rojo, verde, azul):

    # si no se ingresa el nombre de un archivo
    if not filename:
        parser.error('ERROR EN EL ARGUMENTO [-f] [--file]! No se ingreso el nombre de un archivo')

    # si el nombre del archivo no existe
    if os.path.isfile(filename):
        pass
    else:
        #raise FileNotFoundError(f'El archivo {filename} no ha sido encontrado')
        parser.error(f'ERROR EN EL ARGUMENTO [-f] [--file]! El archivo {filename} no ha sido encontrado')
    
    # si el archivo no es ppm
    if not filename.endswith(".ppm"):
        parser.error('ERROR EN EL ARGUMENTO [-f] [--file]! El archivo ingresado no es .ppm')

    # si el n ingresado es negativo
    if size < 0:
        parser.error('ERROR EN EL ARGUMENTO [-n] ! El tamano del bloque a leer no puede ser un numero negativo.')

if __name__ == '__main__':

    # creo los argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', action='store', help='Nombre del archivo', required=True)
    parser.add_argument('-n', type=int, help='Tamano del bloque')
    parser.add_argument('-r', '--red', type=float, help='Escalar color rojo', default=1)
    parser.add_argument('-g', '--green', type=float, help='Escalar color verde', default=1)
    parser.add_argument('-b', '--blue', type=float, help='Escalar color azul', default=1)
    args = parser.parse_args()

    # MANEJO DE ERRORES
    manejo_de_errores(parser, args.file, args.n, args.red, args.green, args.blue)

    # imprimo los argumentos
    #print (args)

    #fd = os.open(f'{args.file}', os.O_RDWR)
    fd = open(f'{args.file}', 'rb')
    chunk_sz = int(args.n)
    escala_rojo = args.red
    escala_verde = args.green
    escala_azul = args.blue

    # creo los archivos de filtros 
    filtro_rojo = open(f'r_{args.file}', 'w')
    filtro_verde = open(f'g_{args.file}', 'w')
    filtro_azul = open(f'b_{args.file}', 'w')

    # leo el archivo completo
    leido = fd.read()
    cuerpo = quitar_header(leido)
    
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
        p = multiprocessing.Process(target=crear_filtros, args=(child_pipe, args.file, chunk_sz, color, rojo, verde, azul, escala_rojo, escala_verde, escala_azul))
        p.start() # inicializo el hijo
        procesos.append(p)

    # leer archivo y escribir al pipe de a chunks
    new_file = open(f'{args.file}_copy', 'rb') 
    while True:
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
    filtro_rojo.close()
    filtro_verde.close()
    filtro_azul.close()
    new_file.close()
    child_pipe.close()
    for i in pipes:
        i.close()
    print("\nSe generaron correctamente los 3 archivos\n")