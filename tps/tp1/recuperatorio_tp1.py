#!/usr/bin/python3
import argparse
import multiprocessing
from collections import Counter
import os

rojo = list()
verde = list()
azul = list()

def read_and_dump(pipe, chunk_sz, escala_rojo, escala_verde, escala_azul):
    while True:
        chunk = pipe.recv() # recive el chunk que envie
        for x in range(0, len(chunk), 3): # para x desde 0 hasta el largo del bloque, leer de a 3 posiciones
            intensidad = chunk[x] * escala_rojo
            if intensidad > 255:
                intensidad = 255
            rojo.append(round(intensidad))
        for x in range(1, len(chunk), 3):
            intensidad = chunk[x] * escala_verde
            if intensidad > 255:
                intensidad = 255
            verde.append(round(intensidad))
        for x in range(2, len(chunk), 3):
            intensidad = chunk[x] * escala_azul
            if intensidad > 255:
                intensidad = 255
            azul.append(round(intensidad))
        if len(chunk) < chunk_sz:
            break
    pipe.close()
    return rojo, verde, azul

def crear_filtros(pipe, filename, chunk_sz, color, escala_rojo, escala_verde, escala_azul):
    rojo, verde, azul = read_and_dump(pipe, chunk_sz, escala_rojo, escala_verde, escala_azul) # tomo las listas rojo, verde y azul
    if color == 'red':
        filtro_rojo = open(f'r_{filename}', 'w') # creo el archivo para guardar el filtro de rojos
        rojo.sort()
        f_rojo = Counter(rojo)
        rojo_ordenado = sorted(f_rojo.items())
        for tupla in rojo_ordenado:
            filtro_rojo.write(str(tupla) + '\n') # escribo el resultado en el archivo que cree anteriormente
    
    elif color == 'green':
        filtro_verde = open(f'g_{filename}', 'w')
        verde.sort()
        f_verde = Counter(verde)
        verde_ordenado = sorted(f_verde.items())
        for tupla in verde_ordenado:
            filtro_verde.write(str(tupla) + '\n')

    elif color == 'blue':
        filtro_azul = open(f'b_{filename}', 'w')
        azul.sort()
        f_azul = Counter(azul)
        azul_ordenado = sorted(f_azul.items())
        for tupla in azul_ordenado:
            filtro_azul.write(str(tupla) + '\n')

def quitar_header(leido):
    # quito los comentarios
    for i in range(leido.count(b"\n# ")):
        comienzo_comentario = leido.find(b"\n# ") # busca la posicion del primer \n# 
        sgte_enter = leido.find(b"\n", comienzo_comentario + 1) # busca la posicion del primer \n que le sigue al encontrado anteriormente
        leido = leido.replace(leido[comienzo_comentario:sgte_enter], b"") # reemplaza por un byte vacio todo lo que este entre la posicion del comienzo del comentario y la del \n que le sigue

    # encontrar encabezado
    primer_enter = leido.find(b"\n") # busca la posicion del primer \n
    segundo_enter = leido.find(b"\n", primer_enter + 1) # busca la posicion del \n que le sigue al anterior
    ultimo_enter = leido.find(b"\n", segundo_enter + 1) # busca la posicion del siguiente \n que sera el ultimo del encabezado
    #encabezado = leido[:ultimo_enter].decode()  # guarda todo lo que esta antes del ultimo enter

    # guardo el cuerpo
    cuerpo = leido[ultimo_enter + 1:] # guarda todo lo que esta despues del ultimo enter
    new_file = open(f'{args.file}'.replace('.ppm', '_copy.ppm'), 'wb')
    new_file.write(cuerpo)
    new_file.close()
    fd.close()
    return cuerpo

def manejo_de_errores(parser, filename, size):

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

    # si el s ingresado es negativo
    if size < 0:
        parser.error('ERROR EN EL ARGUMENTO [-n] ! El tamano del bloque a leer no puede ser un numero negativo.')

if __name__ == '__main__':

    # creo los argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', action='store', help='Nombre del archivo', required=True)
    parser.add_argument('-s', '--size', type=int, help='Tamano del bloque')
    parser.add_argument('-r', '--red', type=float, help='Escalar color rojo', default=1)
    parser.add_argument('-g', '--green', type=float, help='Escalar color verde', default=1)
    parser.add_argument('-b', '--blue', type=float, help='Escalar color azul', default=1)
    args = parser.parse_args()

    # MANEJO DE ERRORES
    manejo_de_errores(parser, args.file, args.size)

    # imprimo los argumentos
    #print (args)

    #fd = os.open(f'{args.file}', os.O_RDWR)
    fd = open(f'{args.file}', 'rb')
    chunk_sz = int(args.size)
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
    for color in colores: # esto es para que se cree un hijo por cada color (3 hijos)
        parent_pipe, child_pipe = multiprocessing.Pipe()
        pipes.append(parent_pipe)
        p = multiprocessing.Process(target=crear_filtros, args=(child_pipe, args.file, chunk_sz, color, escala_rojo, escala_verde, escala_azul))
        p.start() # inicializo el hijo
        procesos.append(p)

    # leer archivo y escribir al pipe de a chunks
    new_file = open(f'{args.file}'.replace('.ppm','_copy.ppm'), 'rb') 
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

    # padre imprime creacion exitosa
    print("\nSe generaron correctamente los 3 archivos\n")

    # bonus track
    if os.path.isfile('filtros'):
        os.remove('filtros')
    tres_filtros = open('filtros', 'a')
    letras_colores = ['r', 'g', 'b']
    for letra in letras_colores:
        if letra == 'r':
            tres_filtros.write('FILTRO ROJO\n-----------\n')
        if letra == 'g':
            tres_filtros.write('\nFILTRO VERDE\n------------\n')
        if letra == 'b':
            tres_filtros.write('\nFILTRO AZUL\n-----------\n')
        tres_filtros.write(open(f'{letra}_{args.file}', 'r').read())

