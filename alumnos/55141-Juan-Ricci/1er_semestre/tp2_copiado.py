#!/usr/bin/python3
import argparse
from array import array
import os
import threading

def multiplo3(num):
    aprox=int(num-(num%3))
    return aprox

def header_size(fd):
    lectura = os.read(fd, 50)
    lectura = (lectura.split(b'\n'))  
    size = 0
    for i in range(len(lectura)):
        if lectura[i-1] == b'255':   
            break
        size += (len(lectura[i])+1)   
    os.lseek(fd, 0, 0)
    return size

def new_header(fd):
    size=header_size(fd)
    header = os.read(fd,size)
    os.lseek(fd,0,0)
    header = str(header, 'utf-8')
    header = header.splitlines()
    new_header=str()
    for i in header:
        if '#' not in i:
            if ' ' in i:
                dim = i.split(' ')
                new_ancho = int(dim[1])
                new_alto = int(dim[0])
                dim_rotadas = str(dim[1]+' '+dim[0])
                new_header = new_header+dim_rotadas+"\n"
            else:
                new_header= new_header+i+"\n"
    new_header = bytes(new_header,'utf-8')
    return new_header,new_ancho,new_alto
    
def generar_matriz(ancho,alto):
    matriz = [[[0,0,0] for _ in range(ancho)]for _ in range(alto)]
    return matriz
    
def rotar_r(alto):
    global matriz
    global pixels
    global columna_r
    global fila_r
    global is_last_chunk
    while True:
        creo_chunk_r.wait()
        creo_chunk_r.clear()
        for i in range(0,len(pixels)-1,3):
            matriz[fila_r][columna_r][0] = pixels[i]
            fila_r-=1
            if fila_r == -1:
                fila_r = alto -1 
                columna_r += 1
        if is_last_chunk == True:
            uso_chunk_r.set()
            break
        uso_chunk_r.set()
        

def rotar_g(alto):
    global matriz
    global pixels
    global columna_g
    global fila_g
    global is_last_chunk
    while True:
        creo_chunk_g.wait()
        creo_chunk_g.clear()
        for i in range(1,len(pixels),3):
            matriz[fila_g][columna_g][1] = pixels[i]
            fila_g-=1
            if fila_g == -1:
                fila_g = alto -1 
                columna_g += 1
        if is_last_chunk == True:
            uso_chunk_g.set()
            break
        uso_chunk_g.set()
        
        
def rotar_b(alto):
    global matriz
    global pixels
    global columna_b
    global fila_b
    global is_last_chunk
    while True:
        creo_chunk_b.wait()
        creo_chunk_b.clear()
        for i in range(2,len(pixels),3):
            matriz[fila_b][columna_b][2] = pixels[i]
            fila_b-=1
            if fila_b == -1:
                fila_b = alto -1 
                columna_b += 1
        if is_last_chunk == True:
            uso_chunk_b.set()
            break
        uso_chunk_b.set()
        



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TP" - Rota imagen ppm')
    parser.add_argument('-n', '--valor',action="store", type= int, required=True, help="Bloque de lectura(Preferentemente un numero multiplo de 3)")
    parser.add_argument('-f', '--file',action="store", required=True, type=str, help="Imagen que se usara")
    args =  parser.parse_args()
    #Chequeo que el archivo que voy a rotar exista
    try:
        foto = os.open(args.file, os.O_RDONLY)
    except FileNotFoundError as err:
        print("No se encontro el archivo a rotar")

    #Abro el archivo y obtengo el nuevo header con su altura y ancho
    foto = os.open(args.file,os.O_RDONLY)
    size = multiplo3(args.valor)
    header,ancho,alto = new_header(foto)
    #Creo el archivo nuevo y le escribo el header nuevo
    archivo_new = str("rotated_"+args.file)
    imagen_rotada = os.open(archivo_new,os.O_RDWR | os.O_CREAT)
    header,ancho,alto = new_header(foto)
    os.write(imagen_rotada,header)
    os.lseek(foto,header_size(foto),0)
    #Creo la matriz que indica los pixeles con valores en 0
    matriz = generar_matriz(ancho,alto)
    pixels = list()
    #Inicializo un flag para ver si lo leido es el ultimo bloque y asi terminar el hilo
    is_last_chunk = False
    #Creo las variables donde iterara la matriz
    columna_r = 0
    columna_g = 0
    columna_b = 0
    fila_r = alto - 1
    fila_g = alto - 1
    fila_b = alto - 1
    #Creo los flags para la concurrencia
    creo_chunk_r = threading.Event()
    creo_chunk_g = threading.Event()
    creo_chunk_b = threading.Event()
    uso_chunk_r = threading.Event()
    uso_chunk_g = threading.Event()
    uso_chunk_b = threading.Event()
    #Establezco las condiciones para iniciar los hilos
    creo_chunk_r.clear()
    creo_chunk_g.clear()
    creo_chunk_b.clear()
    uso_chunk_r.set()
    uso_chunk_g.set()
    uso_chunk_b.set()
    #Creo los hilos y los pongo a correr
    manejador_r = threading.Thread(target=rotar_r,args=(alto,))
    manejador_g = threading.Thread(target=rotar_g,args=(alto,))
    manejador_b = threading.Thread(target=rotar_b,args=(alto,))

    manejador_r.start()
    manejador_g.start()
    manejador_b.start()

    while True:
        uso_chunk_r.wait()
        uso_chunk_g.wait()
        uso_chunk_b.wait()
        chunk = os.read(foto,size)
        uso_chunk_r.clear()
        uso_chunk_g.clear()
        uso_chunk_b.clear()
        pixels=list()
        for i in chunk:
            pixels.append(bytes([i]))
        creo_chunk_r.set()
        creo_chunk_g.set()
        creo_chunk_b.set()
        if len(chunk) < size and b'' in chunk:
            is_last_chunk = True
            break

    manejador_r.join()
    manejador_g.join()
    manejador_b.join()
    #Una vez terminaron de ejecutarse los hijos escribimos la matriz rotada en el archivo
    cont = 0
    for i in matriz:
        valores_rotados = b''
        for j in i:
            for k in j:
                cont += 1
                valores_rotados = valores_rotados + bytes(k)
        os.write(imagen_rotada,valores_rotados)

    archivo = open("matriz_correcta.txt", 'w')
    archivo.write(str(matriz))

    print(cont)
