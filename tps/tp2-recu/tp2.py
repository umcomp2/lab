#!/usr/bin/python3

import argparse
import re
import time
import threading


#Funcion para leer el encabezado 
def leer_encabezado(extension):
    numero_magico = ""
    ancho = 0
    alto = 0
    maxVal = 0

    with open(args.archivo,"rb") as file:
        header = file.readline().strip()
        if header == b"P6":
            numero_magico = header

        while True:
            header = file.readline().strip()
            if header.startswith(b"#"):
                continue
            patron = re.compile(br'^(\d+) (\d+)$') #Valido el alto y ancho de la imagen
            resultado = patron.findall(header)
            break
        ancho = resultado[0][0]
        alto = resultado[0][1]
        header = file.readline().strip()
        maxVal = header
            
    return numero_magico, ancho, alto, maxVal

def leer_raster(archivo, size):
    global matriz
    Numero_magico, ancho, alto, maxVal = leer_encabezado(archivo)
    with open(archivo, "rb") as file:
        while True:
            head = file.readline().strip()
            if head == Numero_magico:
                continue
            elif head.startswith(b"#"):
                continue
            elif head == ancho:
                continue
            elif head == alto:
                continue
            elif head == maxVal:
                continue
            break
        file.readline().strip()
        lista_rojos = []
        lista_verdes = []
        lista_azules = []
        while True:
            raster = file.read(size)
            if len(raster) == 0:
                break
            for i in range(0, len(raster)-1, 3):
                x = raster[i:i+3]
                lista_rojos.append(x[0])
                lista_verdes.append(x[1])
                lista_azules.append(x[2])
    matriz = [[["R","G","B"] for x in range(int(ancho))]for y in range(int(alto))]
    return lista_rojos, lista_verdes, lista_azules, ancho, alto
    

barrera = threading.Barrier(3)

def insertar_encabezado(nombre):
    header = leer_encabezado(nombre)
    #Creo un archivo para guardar el contenido
    archivo = open("imagenespejada" + nombre, "wb")
    for i in header:
        archivo.write(i)
        archivo.write(b"\n")
    archivo.close()

def red(nombre, size):
    global matriz
    insertar_encabezado(nombre)
    archivo = open("imagenespejada" + nombre, "ab")
    rojos,g,b,ancho, alto = leer_raster(nombre, size)
    lista_final_rojos = []

    for i in range(0,len(rojos),int(ancho)):
        pix = rojos[i:i+int(ancho)]
        lista_final_rojos.append(pix[::-1])
    for i in range(int(alto)):
        for j in range(int(ancho)):
            barrera.wait()
            matriz[i][j][0] = lista_final_rojos[i][j]

    

def green(nombre, size):
    global matriz
    r,g,b,ancho, alto = leer_raster(nombre, size)
    verdes = g
    
    lista_final_verdes = []
    
    for i in range(0,len(verdes),int(ancho)):
        pix = verdes[i:i+int(ancho)]
        lista_final_verdes.append(pix[::-1])

    for i in range(int(alto)):
        for j in range(int(ancho)):
            barrera.wait()
            matriz[i][j][1] = lista_final_verdes[i][j]


def blue(nombre, size):
    global matriz
    r,g,b,ancho, alto = leer_raster(nombre, size)
    azules = b
    
    lista_final_azules = []
    
    for i in range(0,len(azules),int(ancho)):
        pix = azules[i:i+int(ancho)]
        lista_final_azules.append(pix[::-1])

    for i in range(int(alto)):
        for j in range(int(ancho)):
            barrera.wait()
            matriz[i][j][2] = lista_final_azules[i][j]




if __name__ == "__main__":

    #Manejador de argumentos
    parser = argparse.ArgumentParser(description="TP1 -f imagen.ppm")
    parser.add_argument('-f',"--file",dest="archivo", action="store", type=str,
                    required=True, help="bits de imagen a leer")
    parser.add_argument('-s', '--size', dest="size", required=True, type=int,
                    help='cantidad de bytes a leer.')
    args = parser.parse_args()
    args.size = args.size - (args.size%3) #reajusta a multiplo de 3

    #Manejo de errores

    if args.size < 0:
        print("Error: no puede ingresar un número negativo")
        exit(1)
    try:
        fd = open(args.archivo, "rb")
    except FileNotFoundError as err:
        print("Error: no es un archivo ppm")
        exit(1)

    #Creo los 3 hijos
    threads = []
    hilo_r = threading.Thread(target = red, args = (args.archivo,args.size,))
    hilo_g = threading.Thread(target = green, args = (args.archivo,args.size,))
    hilo_b = threading.Thread(target = blue, args = (args.archivo,args.size,))

    threads.append(hilo_r)
    threads.append(hilo_g)
    threads.append(hilo_b)

    # Starteo los hilos
    for h in threads:
        h.start()

    for h in threads:
        h.join()

    archivo = open("imagenespejada" + args.archivo, "ab")
    for i in matriz:
        for j in i:
            archivo.write(bytes(j))
    time.sleep(2)
    print("Imagen espejada gracias a dios")
