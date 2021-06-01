#!/usr/bin/python3

import argparse
import multiprocessing as mp
import re
import time

def leer_encabezado(archivo):
    #rb = Abrir fichero de lectura en binario
    with open(archivo, "rb") as header:
        head = header.readline().strip()
        if head == b"P6":
            Numero_magico = head
        while True:
            head = header.readline().strip()
            if head.startswith(b"#"):
                continue
            patron = re.compile(br'^([0-9]+) ([0-9]+)$')
            anchura = patron.findall(head)
            break
        Anchura = anchura[0][0]
        Altura = anchura[0][1]
        head = header.readline().strip()
        MaxVal = head
        #print("----------ENCABEZADO----------\n")
        #print(f"Numero magico----->{Numero_magico}")
        #print(f"Anchura----->{Anchura}")
        #print(f"Altura----->{Altura}")
        #print(f"MaxVal----->{MaxVal}")
    return Numero_magico, Anchura, Altura, MaxVal

def leer_raster(archivo, cola, size):
    Numero_magico, Anchura, Altura, MaxVal = leer_encabezado(archivo)
    with open(archivo, "rb") as header:
        while True:
            head = header.readline().strip()
            if head == Numero_magico:
                continue
            elif head.startswith(b"#"):
                continue
            elif head == Anchura:
                continue
            elif head == Altura:
                continue
            elif head == MaxVal:
                continue
            break
        header.readline().strip()
        while True:
            raster = header.read(size)
            cola.put(raster)
            if len(raster) == 0:
                break
    return raster

def hijo_r(nombre, cola_r, size, cond_r):
    header = leer_encabezado(nombre)
    #Creo un archivo para guardar el contenido
    archivo = open("Rojo_" + nombre,"wb")
    for i in header:
        archivo.write(i+b"\n")
    raster = leer_raster(nombre, cola_r, size)
    l = 0
    list_r = []
    while True:
        r = cola_r.get()
        for i in r:
            list_r.append(i)
        largo = l + len(r)
        if len(raster) == largo:
            break
    for i in range(0, len(list_r)-1, 3):
        pix = list_r[i:i+3] 
        pix[0] = round(pix[0] * cond_r)
        if pix[0] > 255:
            pix[0] = 255
        else:
            pix[0] = pix[0]
        pix[1] = 0
        pix[2] = 0
        archivo.write(bytes(pix))


def hijo_g(nombre, cola_g, size, cond_g):
    header = leer_encabezado(nombre)
    #Creo un archivo para guardar el contenido
    archivo = open("Verde_" + nombre,"wb")
    for i in header:
        archivo.write(i+b"\n")
    raster = leer_raster(nombre, cola_g, size)
    l = 0
    list_g = []
    while True:
        r = cola_g.get()
        for i in r:
            list_g.append(i)
        largo = l + len(r)
        if len(raster) == largo:
            break
    for i in range(0, len(list_g)-1, 3):
        pix = list_g[i:i+3]
        pix[0] = 0
        pix[1] = round(pix[1] * cond_g)
        if pix[1] > 255:
            pix[1] = 255
        else:
            pix[1] = pix[1]
        pix[2] = 0
        archivo.write(bytes(pix))


def hijo_b(nombre, cola_b, size, cond_b):
    header = leer_encabezado(nombre)
    #Creo un archivo para guardar el contenido
    archivo = open("Azul_" + nombre,"wb")
    for i in header:
        archivo.write(i+b"\n")
    raster = leer_raster(nombre, cola_b, size)
    l = 0
    list_b = []
    while True:
        r = cola_b.get()
        for i in r:
            list_b.append(i)
        largo = l + len(r)
        if len(raster) == largo:
            break
    for i in range(0, len(list_b)-1, 3):
        pix = list_b[i:i+3]
        pix[0] = 0
        pix[1] = 0
        pix[2] = round(pix[2] * cond_b)
        if pix[2] > 255:
            pix[2] = 255
        else:
            pix[2] = pix[2]
        archivo.write(bytes(pix))


if __name__=="__main__":

    #Argumentos
    parser = argparse.ArgumentParser(description='Trabajo practico 1-recuperatorio')
    parser.add_argument('-f', '--file', dest = "archivo", required = True, help = "Archivo a procesar")
    parser.add_argument('-n', '--size', dest = "size", required = True, type=int, help = "Bloque de lectura")
    parser.add_argument('-r', '--red', dest = "red", default=1, type=float, help = "Escala para el rojo")
    parser.add_argument('-g', '--green',dest = "green", default=1, type=float, help = "Escala para el verde")
    parser.add_argument('-b', '--blue', dest = "blue", default=1, type=float, help = "Escala para el azul")

    args = parser.parse_args()

    try:
        arch = open(args.archivo, "r")
    except FileNotFoundError:
        print("El archivo no existe")
        exit()
        
    #Condicion para que solo se pueda ingresar un imagen .ppm
    if ".ppm" not in args.archivo:
        print("ERROR: no es una imagen ppm")
        exit()

    #Condicion para que size no pueda ser negativo
    if args.size < 0:
        print("ERROR: el size no puede ser negativo")
        exit()
    
    #Condicion para que las escalas (-r -g y -b) no puedan ser negativas
    if args.red < 0 or args.green < 0 or args.blue < 0:
        print("ERROR: la escala (-r -g o -b) no pueden ser negativas")
        exit()

    args.size = args.size - (args.size%3) #reajusta a multiplo de 3

    #Creacion de IPC
    q_r = mp.Queue()
    q_g = mp.Queue()
    q_b = mp.Queue()

    lista_hijos = []
    #Creacion de hijos
    hijo_r = mp.Process(target=hijo_r, args=(args.archivo, q_r, args.size, args.red, ))
    lista_hijos.append(hijo_r)
    hijo_g = mp.Process(target=hijo_g, args=(args.archivo, q_g, args.size, args.green, ))
    lista_hijos.append(hijo_g)
    hijo_b = mp.Process(target=hijo_b, args=(args.archivo, q_b, args.size, args.blue, ))
    lista_hijos.append(hijo_b)

    #Iniciar hijos
    for i in lista_hijos:
        time.sleep(2)
        print("Iniciando hijo...")
        i.start()
    
    #Esperemos a los hijos
    for i in lista_hijos:
        i.join()