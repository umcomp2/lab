#!/usr/bin/python3

import argparse
import threading as th
import re

barrera = th.Barrier(3)

def leer_encabezado(archivo):
    #rb = Abrir fichero de lectura en binario
    with open(archivo, "rb") as header:
        head = header.readline().strip()
        if head == b"P6" or b"P3":
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
        MaxVal = header.readline().strip()
        #print("----------ENCABEZADO----------\n")
        #print(f"Numero magico----->{Numero_magico}")
        #print(f"Anchura----->{Anchura}")
        #print(f"Altura----->{Altura}")
        #print(f"MaxVal----->{MaxVal}")
    return Numero_magico, Anchura, Altura, MaxVal

def multifuncion(archivo, size):
    global matriz
    #Comparamos el encabezado y leemos el cuerpo del raster
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
        lista_r = []
        lista_v = []
        lista_a = []
        while True:
            raster = header.read(size)
            if len(raster) == 0:
                break
            for i in range(0, len(raster)-1, 3):
                pix = raster[i:i+3]
                lista_r.append(pix[0])
                lista_v.append(pix[1])
                lista_a.append(pix[2])
    matriz = [[["R","V","A"] for x in range(int(Anchura))]for y in range(int(Altura))]
    return lista_r, lista_v, lista_a, Anchura, Altura
                         
def abrir_arch(archivo):
    header = leer_encabezado(archivo)
    #Creo un archivo para guardar el contenido
    archivo = open("espejado_" + archivo,"wb")
    for i in header:
        archivo.write(i+b"\n")   

def hilo_rojo(archivo, tamaño):
    global matriz
    r, v, a, Anchura, Altura = multifuncion(archivo, tamaño)
    roja = []
    for i in range(0, len(r), int(Anchura)):
        x = r[i:i+int(Anchura)]
        roja.append(x)
    for i in roja:
        i.reverse()
    for i in range(int(Altura)):
        for j in range(int(Anchura)):
            barrera.wait()
            matriz[i][j][0] =  roja[i][j]

def hilo_verde(archivo, tamaño):
    global matriz
    r, v, a, Anchura, Altura = multifuncion(archivo, tamaño)
    verde = []
    for i in range(0, len(v), int(Anchura)):
        y = v[i:i+int(Anchura)]
        verde.append(y)
    for i in verde:
        i.reverse()
    for i in range(int(Altura)):
        for j in range(int(Anchura)):
            barrera.wait()
            matriz[i][j][1] =  verde[i][j]

def hilo_azul(archivo, tamaño):
    global matriz
    r, v, a, Anchura, Altura = multifuncion(archivo, tamaño)
    azul = []
    for i in range(0, len(a), int(Anchura)):
        z = a[i:i+int(Anchura)]
        azul.append(z)
    for i in azul:
        i.reverse()
    for i in range(int(Altura)):
        for j in range(int(Anchura)):
            barrera.wait()
            matriz[i][j][2] =  azul[i][j]

def funcion_final(archivo):
    global matriz
    abrir_arch(archivo)
    archivo_or = open("espejado_"+ archivo, "ab")
    for i in matriz:
        for j in i:
            archivo_or.write(bytes(j))


if __name__=="__main__":

    #Argumentos
    parser = argparse.ArgumentParser(description='Trabajo practico 2-recuperatorio')
    parser.add_argument('-f', '--file', dest = "archivo", required = True, help = "Archivo a procesar")
    parser.add_argument('-n', '--size', dest = "size", required = True, type=int, help = "Bloque de lectura")

    args = parser.parse_args()
    args.size = args.size - (args.size%3) #reajusta a multiplo de 3

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
    
    lista_hijos = []
    #Creacion de hijos
    hilo_r = th.Thread(target=hilo_rojo, args=(args.archivo, args.size, ))
    lista_hijos.append(hilo_r)
    hilo_v = th.Thread(target=hilo_verde, args=(args.archivo, args.size, ))
    lista_hijos.append(hilo_v)
    hilo_a = th.Thread(target=hilo_azul, args=(args.archivo, args.size, ))
    lista_hijos.append(hilo_a)

    #Iniciar hijos
    for i in lista_hijos:
        print("Iniciando hijo...")
        i.start()
    
    #Esperemos a los hijos
    for i in lista_hijos:
        i.join()
    
    funcion_final(args.archivo)

    print("El padre finalizo...")