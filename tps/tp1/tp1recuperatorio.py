#!/usr/bin/python3

import argparse
import re
import time
import multiprocessing


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
        ancho = resultado[0][0] # Ingresamos el resultado de la expresion regular
        alto = resultado[0][1]  # en el diccionario
        
        header = file.readline().strip()
        maxVal = header
            
    return numero_magico, ancho, alto, maxVal

def leer_raster(archivo, size, queue):
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
        while True:
            raster = file.read(size)
            queue.put(raster)
            if len(raster) == 0:
                break
    return raster
    

def hijo_rojo(extension, size, queue_r, escala):
    print(".........Trabajando con los pixeles rojos de la imagen.........")
    time.sleep(1)
    header = leer_encabezado(extension)
    #Creo un archivo para guardar el contenido
    archivo = open("Red_" + extension ,"wb")
    for i in header:
        archivo.write(i)
        archivo.write(b"\n")
    raster = leer_raster(extension, size, queue_r)
    escrito = 0
    red_list = []
    while True: 
        imagen = queue_r.get()
        for i in imagen:
            red_list.append(i)
        largo = escrito + len(imagen)
        if len(raster) == largo:
            break
    for i in range(0,len(red_list)-1,3):
        x = red_list[i:i+3]
        x[0] = round(x[0] * escala)
        if x[0] > 255:
            x[0] = 255
        else:
            x[0] = x[0]
        x[1] = 0
        x[2] = 0
        archivo.write(bytes(x))

def hijo_verde(extension,size, queue_g, escala):
    print(".........Trabajando con los pixeles verdes de la imagen.........")
    time.sleep(1)
    header = leer_encabezado(extension)
    #Creo un archivo para guardar el contenido
    archivo = open("Green_"+ extension, "wb")
    for i in header:
        archivo.write(i)
        archivo.write(b"\n")
    raster = leer_raster(extension, size, queue_g)
    escrito = 0
    green_list = []
    while True:
        imagen = queue_g.get()
        for i in imagen:
            green_list.append(i)
        largo = escrito + len(imagen)
        if len(raster) == largo:
            break
    for i in range(0,len(green_list)-1,3):
        x = green_list[i:i+3]
        x[1] = round(x[1] + escala)
        if x[1] > 255:
            x[1] = 255
        else:
            x[1] = x[1]
        x[0] = 0
        x[2] = 0
        archivo.write(bytes(x))


def hijo_azul(extension, size, queue_b, escala):
    print(".........Trabajando con los pixeles azules de la imagen.........")
    time.sleep(2)
    header = leer_encabezado(extension)
    #Creo un archivo para guardar el contenido
    archivo = open("Blue_" + extension, "wb")
    for i in header:
        archivo.write(i)
        archivo.write(b"\n")
    raster = leer_raster(extension, size, queue_b)
    escrito = 0
    blue_list = []
    while True:
        imagen = queue_b.get()
        for i in imagen:
            blue_list.append(i)
        largo = escrito + len(imagen)
        if len(raster) == largo:
            break
    for i in range(0,len(blue_list)-1,3):
        x = blue_list[i:i+3]
        x[2] = round(x[2] * escala)
        if x[2] > 255:
            x[2] = 255
        else:
            x[2] = x[2]
        x[0] = 0
        x[1] = 0 
        archivo.write(bytes(x))
        
if __name__ == "__main__":

    #Manejador de argumentos
    parser = argparse.ArgumentParser(description="TP1 -f imagen.ppm")
    parser.add_argument('-f',"--file",dest="archivo", action="store", type=str,
                    required=True, help="bits de imagen a leer")
    parser.add_argument('-s', '--size', dest="size", required=True, type=int,
                    help='cantidad de bytes a leer.')
    parser.add_argument('-r', '--red', dest = "red", default = 1, type = float,
                    help = "escala para el rojo")
    parser.add_argument('-g', '--green',dest = "green", default = 1, type = float,
                    help = "escala para el verde")
    parser.add_argument('-b', '--blue', dest = "blue", default = 1, type = float,
                    help = "escala para el azul")
    args = parser.parse_args()
    args.size = args.size - (args.size%3) #reajusta a multiplo de 3

    #Manejo de errores
    if args.red < 0:
        print("Error: no puede ingresar un número negativo")
        exit(1)
    if args.green < 0:
        print("Error: no puede ingresar un número negativo")
        exit(1)
    if args.blue < 0:
        print("Error: no puede ingresar un número negativo")
        exit(1)
    if args.size < 0:
        print("Error: no puede ingresar un número negativo")
        exit(1)
    try:
        fd = open(args.archivo, "rb")
    except FileNotFoundError as err:
        print("Error: no es un archivo ppm")
        exit(1)


    #Creo las colas para los hijos
    q_red = multiprocessing.Queue()
    q_green = multiprocessing.Queue()
    q_blue = multiprocessing.Queue()

    #Creo los hijos
    lista_hijos = []
    hijo_rojo = multiprocessing.Process(target=hijo_rojo, args = (args.archivo,args.size, q_red, args.red))
    hijo_verde = multiprocessing.Process(target=hijo_verde, args = (args.archivo,args.size, q_green, args.green))
    hijo_azul = multiprocessing.Process(target=hijo_azul, args = (args.archivo,args.size, q_blue,args.blue))
    lista_hijos.append(hijo_rojo)
    lista_hijos.append(hijo_verde)
    lista_hijos.append(hijo_azul)
 
    for i in lista_hijos:
        i.start()
        i.join()
    print("El proceso padre terminó")