#!/usr/bin/python3

import argparse
import multiprocessing as mp
import os
import re

def hijo_rojo(conn):

    #Creo una lista para almacenar los pixeles
    pixeles_rojo = []
    #Creo un archivo para guardar el contenido
    archivo = open("Rojo.txt","wt")
    while True:
        contenido = conn.recv()
        if contenido == b'EOF':
            break
        for i in range(0,len(contenido), 3):
            pix = contenido[i:i+3]
            pixeles_rojo.append(pix[0])
    archivo.write(str(dict(enumerate(pixeles_rojo))))
    conn.close()
    archivo.close()

def hijo_verde(conn):

    #Creo una lista para almacenar los pixeles
    pixeles_verde = []
    #Creo un archivo para guardar el contenido
    archivo = open("Verde.txt","wt")
    while True:
        contenido = conn.recv()
        if contenido == b'EOF':
            break
        for i in range(0,len(contenido), 3):
            pix = contenido[i:i+3]
            pixeles_verde.append(pix[1])
    archivo.write(str(dict(enumerate(pixeles_verde))))
    conn.close()
    archivo.close()

def hijo_azul(conn):

    #Creo una lista para almacenar los pixeles
    pixeles_azul = []
    #Creo un archivo para guardar el contenido
    archivo = open("Azul.txt","wt")
    while True:
        contenido = conn.recv()
        if contenido == b'EOF':
            break
        for i in range(0,len(contenido), 3):
            pix = contenido[i:i+3]
            pixeles_azul.append(pix[2])
    archivo.write(str(dict(enumerate(pixeles_azul))))
    conn.close()
    archivo.close()

if __name__=="__main__":

    #Argumentos
    parser = argparse.ArgumentParser(description='Trabajo practico 1')
    parser.add_argument('-f', '--file', dest = "archivo", help = "imagen a leer")
    parser.add_argument('-n', dest = "bytes", type = int, help = "bloque a leer")

    args = parser.parse_args()

    #Condicion para que solo se pueda ingresar un imagen .ppm
    if ".ppm" not in args.archivo:
        print("ERROR: no es una imagen ppm")
        exit()

    list_pipes_padres = []
    #Creacion de IPC
    parent_r, child_r = mp.Pipe()
    list_pipes_padres.append(parent_r)
    parent_v, child_v = mp.Pipe()
    list_pipes_padres.append(parent_v)
    parent_a, child_a = mp.Pipe()
    list_pipes_padres.append(parent_a)

    lista_hijos = []
    #Creacion de hijos
    hijo_r = mp.Process(target=hijo_rojo,  args=(child_r, ))
    lista_hijos.append(hijo_r)
    hijo_v = mp.Process(target=hijo_verde,  args=(child_v, ))
    lista_hijos.append(hijo_v)
    hijo_a = mp.Process(target=hijo_azul,  args=(child_a, ))
    lista_hijos.append(hijo_a)

    #Iniciar hijos
    for i in lista_hijos:
        i.start()

    #obtener el encabezado
    dict_header = {
        "Numero_magico": None,
        "Anchura": 0,
        "Altura": 0,
        "MaxVal": 0
        }
    with open(args.archivo, "rb") as header: #rb = Abrir fichero de lectura en binario
        head = header.readline().strip()
        if head == b"P6":
            dict_header["Numero_magico"] = head
        while True:
            head = header.readline().strip()
            if head.startswith(b"#"):
                continue
            patron = re.compile(br'^([0-9]+) ([0-9]+)$')
            anchura = patron.findall(head)
            break
        dict_header["Anchura"] = anchura[0][0]
        dict_header["Altura"] = anchura[0][1]
        head = header.readline().strip()
        dict_header["MaxVal"] = head

        #print("\n----Encabezado----\n")
        #for a in dict_header.items():
            #print(a)
        
        #leer los bloques segun -n
        while (bloque_leer:= header.read(args.bytes).strip()):
            for pipe_padre in list_pipes_padres:
                pipe_padre.send(bloque_leer)
            if len(bloque_leer) == 0:
                break
        
    for pipe_padre in list_pipes_padres:
        pipe_padre.send(b'EOF')

    #El padre espera a los hijos
    for hijos in lista_hijos:
        hijos.join()

    #Cerrar archivo
    header.close()
    #Cerrar pipes padres
    for i in list_pipes_padres:
        i.close()

    print("-------->Termino el padre<--------")