#!/usr/bin/python3
<<<<<<< HEAD

import argparse
import os
import re
import multiprocessing
import time


def hijo_rojo(pipe):

    lista_rojo = []
    archivo = open("Rojo.txt", "wt")
    while True:
        a = pipe.recv()
        if a == b'EOF':
            break
        for i in range(0,len(a), 3):
            pixel = a[i:i+3]
            lista_rojo.append(pixel[0])
    
    archivo.write(str(dict(enumerate(lista_rojo))))

    pipe.close()
    archivo.close()

def hijo_verde(pipe):
    lista_verde = []
    archivo = open("Verde.txt", "wt")
    while True: 
        b = pipe.recv()
        if b == b'EOF':
            break
        for i in range(0,len(b),3):
            pixel = b[i:i+3]
            lista_verde.append(pixel[1])
    archivo.write(str(dict(enumerate(lista_verde))))

    pipe.close()
    archivo.close()
    

def hijo_azul(pipe):
    lista_azul = []
    archivo = open("Azul.txt", "wt")
    while True:
        c = pipe.recv()
        if c == b'EOF':
            break
        for i in range(0,len(c),3):
            pixel = c[i:i+3]
            lista_azul.append(pixel[2])
    archivo.write(str(dict(enumerate(lista_azul))))

    pipe.close()
    archivo.close()

if __name__ == "__main__":

    #Manejador de argumentos, -f --file, -s --size
    parser = argparse.ArgumentParser(description="TP1 -f imagen.ppm")
    parser.add_argument('-f',"--file",dest="archivo", action="store", metavar="archivo", type=str,
                    required=True, help="bits de imagen a leer")
    parser.add_argument('-s', '--size', dest="size", required=True, type=int, metavar='bloque de lectura',
                    help='Ingrese cantidad de bytes a leer.')
    args = parser.parse_args()

    #Creo los PIPES de los colores
    list_pipes_parents = []
    red_parent, red_child = multiprocessing.Pipe()
    green_parent, green_child = multiprocessing.Pipe()
    blue_parent, blue_child = multiprocessing.Pipe()
    
    #Agrego los pipes a una lista
    list_pipes_parents.append(red_parent)
    list_pipes_parents.append(green_parent)
    list_pipes_parents.append(blue_parent)

    #Creo los hijos RGB
    list_hijos = []
    hijo_rojo = multiprocessing.Process(target=hijo_rojo, args=(red_child,))
    hijo_verde = multiprocessing.Process(target=hijo_verde, args=(green_child,))
    hijo_azul = multiprocessing.Process(target=hijo_azul, args=(blue_child,))

    list_hijos.append(hijo_rojo)
    list_hijos.append(hijo_verde)
    list_hijos.append(hijo_azul)

    hijo_rojo.start()
    hijo_verde.start()
    hijo_azul.start()

    #Leemos el encabezado
    dict_encabezado = {
        "Numero_magico": None,
        "Ancho":0,
        "Alto":0,
        "MaxVal":0     
    }
    with open(args.archivo,"rb") as file:
        header = file.readline().strip()
        if header == b"P6":
            dict_encabezado["Numero_magico"] = header

        while True:
            header = file.readline().strip()
            if header.startswith(b"#"):
                continue

            patron = re.compile(br'^(\d+) (\d+)$') #Valido el alto y ancho de la imagen
            resultado = patron.findall(header)
            break
        dict_encabezado["Ancho"] = resultado[0][0] # Ingresamos el resultado de la expresion regular
        dict_encabezado["Alto"] = resultado[0][1]  # en el diccionario
        

        header = file.readline().strip()
        dict_encabezado["MaxVal"] = header

        print("\n ........Leyendo datos del encabezado........ \n")
        for valor in dict_encabezado.items():
            print(valor)
            time.sleep(3)

        #Lee los bloques que mencionamos con -s y envia los bytes correspondientes a cada hijo
        while (bloque:= file.read(args.size).strip()):
            for valor in list_pipes_parents:
                valor.send(bloque)
            if len(bloque) == 0:
                break

    #Envío EOF a los hijos
    for pipes in list_pipes_parents:
        pipes.send(b'EOF')
        pipes.close()
    #Espero a que terminen los hijos
    for i in list_hijos:
        i.join()

    print("\nEl padre terminó exitosamente\n")
=======
import os
import argparse
import multiprocessing as mp
import fmanager
import workers

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tp1 - procesa ppm')
    parser.add_argument('-s', '--size',action="store", type= int, required=True, help="Bloque de lectura")
    parser.add_argument('-b', '--bonus',action="store", type= bool, required=False, help="genera archivos con filtros")
    parser.add_argument('-f', '--file',action="store", dest="file", required=True, type=str, help="archivo a procesar")

    args =  parser.parse_args()
    archivo = args.file
    args.size = args.size - (args.size%3) #reajusta a multiplo de 3
    try:
        fd = os.open(archivo, os.O_RDONLY)
    except FileNotFoundError as err:
        print("OS error: {0}".format(err))
        exit(1)
    #manejo de info del encabezado en un modulo
    off,width,height,maxval = fmanager.lee_encabezado(fd)
    os.lseek(fd,off,0) #rebobina al principio del raster
    geometria = [width,height,maxval]
    h = [] #list to save the process
    colors = "rgb"
    for i in colors:
        exec("cola_{} = mp.Queue()".format(i))
        exec('h.append(mp.Process(target=workers.histo, args=(cola_{},i,archivo,geometria,args.bonus)))'.format(i))
        h[-1].start() #el ultimo

    escrito = 0
    while escrito < (width * height * 3): #leyendo de a size ... (si usan mq, el maximo es 32k, si usan pipe , es 8k )
        imorig = os.read(fd, args.size)
        escrito = escrito + len(imorig)
        for i in colors:
            if escrito > (width * height * 3):
                exec('cola_{}.put(imorig[0:(width * height * 3 ) %args.size ])'.format(i)) #por si vienes mas datos que los que corresponden
            else:
                exec('cola_{}.put(imorig)'.format(i))

    for i in range(len(h)):
        h[i].join()
    print ("Se generaron correctamente los" , len(h), "histogramas")
>>>>>>> dd07068ddcaf8138e3eab4d4c4a3ffa57f5a8a07
