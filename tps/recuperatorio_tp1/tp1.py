import argparse
import multiprocessing as mp
from multiprocessing import Process, Queue
import exceptions

#import os
def leer_archivo(archivo, cola, size):
    #ABRIR ARCHIVO 
    try:
        ppm = open(archivo, 'rb')
        #LEER EL ENCABEZADO
        header = []
        if archivo.endswith('.ppm'):
            #El strip()método elimina los caracteres iniciales (espacios al principio) y finales (espacios al final)/
            # (el espacio es el carácter inicial predeterminado para eliminar)
            num_magico = ppm.readline().strip()
            if num_magico == b"P6" or num_magico==b"P3":
                header.append(num_magico)
            else:
                raise exceptions.NoPPMfile

            #Hago un while para evitar que en el encabezado me muestre el "#"
            while True:
                ancho_alto = ppm.readline().strip()
                if ancho_alto.startswith(b"#"):
                    continue
                header.append(ancho_alto)
                break

            val_max = ppm.readline().strip()
            if val_max <= b"255":
                header.append(val_max)
            else:
                print("no puede pasar los 255")
            print(header)
        else:
            raise exceptions.NoPPMfile
        #leer raster
        while True:
            raster = ppm.read(size)
            cola.put(raster)
            #print(cola)
            if len(raster) == 0:
                break
                
            
    except FileNotFoundError:
        print("El archivo no existe")
        exit()
    except exceptions.NoPPMfile:
        print("No es un archivo ppm")
        exit() 
    return num_magico, ancho_alto, val_max, raster


  


def hijos(nombre_archivo, cola, size, escala, color):
    color_name = ""
    color_index = 0 
    if (color == 'r'):
        color_name = "Rojo"
        color_index = 0
    elif (color == 'g'):
        color_name = "Verde"
        color_index = 1
    elif (color == 'b'):
        color_name = "Azul"
        color_index = 2

    num_magico, ancho_alto, val_max, cuerpo = leer_archivo(nombre_archivo, cola, size)
    #header = encabezado(nombre_archivo)
    header = (num_magico, ancho_alto, val_max)
    #Creo un archivo para guardar el contenido
    archivo = open(color_name + "_" + nombre_archivo,"wb")
    for i in header:
        archivo.write(i+b"\n")
    #cuerpo = raster(nombre_archivo, cola, size) 
    contador = 0
    list_colas= []
    while True:
        colas = cola.get()
        for i in colas:
            list_colas.append(i)
        largo = contador + len(colas)
        if len(cuerpo) == largo: #cuando leo toda la imagen q termine
            break
    for i in range(0, len(list_colas)-1, 3):
        pix = [0]*3 #creo una lista de 3 ceros
        pix_ref = list_colas[i:i+3] 
        pix[color_index] = round(pix_ref[color_index] * escala) 
        if pix[color_index] > 255:
            pix[color_index] = 255
        archivo.write(bytes(pix))
    archivo.close() 
        

    

if __name__=="__main__":

    #ARGUMENTOS
    parser = argparse.ArgumentParser(description="TPN°1")
    parser.add_argument('-f', '--file', required=True, help="imagen a procesar",dest="archivo",)
    parser.add_argument('-s', '--size',default=1, type=int, required=True,help='bloque de lectura', dest="size", )
    parser.add_argument('-r', '--red',default=1, type=float, required=False, help='escala para rojo', dest="red")
    parser.add_argument('-g', '--green',default=1, type=float, required=False, help='escala para green', dest="green")
    parser.add_argument('-b', '--blue', default=1, type=float, required=False, help='escala para azul', dest="blue")
    arg = parser.parse_args() 

    #ESCALA (RED, GREEN, BLUE) NO PUEDE SER NEGATIVA
    try:
        if arg.red < 0 or arg.green < 0 or arg.blue < 0:
            raise exceptions.EscalaNoNegativa

    except exceptions.EscalaNoNegativa:
        print("La escala elegida para red, green y blue no puede ser negativa")
        exit()
    
    #Size no negativo
    try:
        if arg.size < 0:
            raise exceptions.SizeNoNegativo
    except exceptions.SizeNoNegativo:
        print("Size no puede ser negativo")
        exit()

    
    
    #IPC-->QUEUE
    q_rojo = Queue()
    q_verde = Queue()
    q_azul = Queue()

    #CREACION DE LOS HIJOS
    lista_hijos= []

    h_rojo = Process(target=hijos, args=(arg.archivo, q_rojo, arg.size, arg.red, "r"))
    h_verde = Process(target=hijos, args=(arg.archivo, q_verde, arg.size, arg.green, "g"))
    h_azul= Process(target=hijos, args=(arg.archivo, q_azul, arg.size, arg.blue, "b"))
    lista_hijos.append(h_rojo)
    lista_hijos.append(h_verde)
    lista_hijos.append(h_azul)
    #iniciar hijos
    for i in lista_hijos:
        i.start()
    #esperar hijos
    for i in lista_hijos:
        i.join()
    

    