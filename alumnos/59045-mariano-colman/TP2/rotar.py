import argparse
import os
import sys
import time
import threading

def get_header(parseo):
    #Abro la imagen y la leo en bytes
    img = open(parseo.file, "rb").read()

    #Con la imagen abierta procedo a reemplazar los comentarios
    for i in range(img.count(b"\n# ")):
        basura1 = img.find(b"\n# ")
        basura2 = img.find(b"\n", basura1 + 1)
        img = img.replace(img[basura1:basura2], b"")
        
    #Calculo la posicion donde se encuentra la delimitacion del header con el body
    limiteHeader = img.find(b"\n", img.find(b"\n", img.find(b"\n")+1)+1)+1
    header = img[:limiteHeader].decode()
    headerLimpio = header.replace("\n", " ")
    altoYancho = []
    for i in headerLimpio.split():
            if len(i) > 2:
                altoYancho.append(i)
    print(altoYancho)
    return img[:limiteHeader], img[limiteHeader:], altoYancho, limiteHeader

def crearMatriz(tamaño):
    matriz = [[[0,0,0] for i in range(int(tamaño[0]))]for i in range(int(tamaño[1]))]
    return matriz

def colorRojo(parseo, fd):
    global barrera
    global nMatriz
    global pos
    global tamaño
    fila = int(tamaño[0]) - 1
    columna = 0
    #os.lseek(fd, pos, 0)
    while True:
        leido = os.read(fd, parseo.size)
        for i in range(0, len(leido)-1, 3):
            #if (i) % 3 == 0 or i == 0:
            nMatriz[fila][columna][0] = bytes([leido[i]])
            #semaforo.release()
            fila -= 1
            if fila < 0:
                fila = int(tamaño[0]) - 1
                columna += 1
            #print("fila"+str(fila))
            #print("columna"+str(columna))
            #print("contador"+str(contador))
        #barrera.wait()
        #print("levante barrera rojo")   
        if len(leido) != parseo.size:
                break

def colorVerde(parseo, fd):
    global barrera
    global nMatriz
    global pos
    global tamaño
    fila = int(tamaño[0]) - 1
    columna = 0
    contador = 0
    #os.lseek(fd, pos, 0)
    while True:
        leido = os.rea  (fd, parseo.size)
        for i in range(1, len(leido), 3):
            #if (i+2) % 3 == 0 or i == 1:
            #semaforo.acquire()
            nMatriz[fila][columna][1] = bytes([leido[i]])
            #semaforo.release()
            contador +=1 
            fila -= 1
            if fila < 0:
                fila = int(tamaño[0]) - 1
                columna += 1
            #print("fila"+str(fila))
            #print("columna"+str(columna))
            #print("contador"+str(contador))
        #barrera.wait()
        #print("levante barrera verde")
        if len(leido) != parseo.size:
                break
    #print(nMatriz)

def colorAzul(parseo, fd):
    global barrera
    global nMatriz
    global pos
    global tamaño
    fila = int(tamaño[0]) - 1
    columna = 0
    contador = 0
    #os.lseek(fd, pos, 0)
    while True:
        leido = os.read(fd, parseo.size)
        for i in range(2, len(leido), 3):
            #if (i+1) % 3 == 0 or i == 2:
            #semaforo.acquire()
            #print(bytes([leido[i]]))
            nMatriz[fila][columna][2] = bytes([leido[i]])
            #semaforo.release()
            contador +=1 
            fila -= 1
            if fila < 0:
                fila = int(tamaño[0]) - 1
                columna += 1
            #print("fila"+str(fila))
            #print("columna"+str(columna))
            #print("contador"+str(contador))
        #barrera.wait()
        #print("levante barrera azul")
        if len(leido) != parseo.size:
                break
    #print(nMatriz)
if __name__ == '__main__':

    try:
        parser = argparse.ArgumentParser(description="Procesamiento de imagenes por colores")

        parser.add_argument("-f", "--file", type=str, required=True, help="Nombre de la imagen")
        parser.add_argument("-s", "--size", type=int, default=1023, help="Valor del bloque a analizar")

        parseo = parser.parse_args()
    except:
        print("Valores ingresados incorrectos")
        sys.exit()
    try:
        if parseo.size <= 0:
            raise ValueError()
    except:
        print("Tamaño de bloque incorrecto")
        sys.exit()
    
    foto = os.open(parseo.file, os.O_RDONLY)
    header, body, tamaño, pos = get_header(parseo)
    img_nueva = str("rotada_"+parseo.file)
    fd = os.open(img_nueva, os.O_RDWR | os.O_CREAT)
    os.write(fd, header)
    nMatriz = crearMatriz(tamaño)
    os.lseek(foto, pos, 0)
    #colorRojo(parseo, foto)
    #colorVerde(parseo, foto)
    #colorAzul(parseo, foto)
    #semaforo = threading.Semaphore(value=0)
    #barrera = threading.Barrier(3)
    hilos = []
    hilos.append(threading.Thread(target=colorRojo, args=(parseo, foto, )))
    hilos.append(threading.Thread(target=colorVerde, args=(parseo, foto, )))
    hilos.append(threading.Thread(target=colorAzul, args=(parseo, foto, )))

    for i in hilos:
        i.start()

    for i in hilos:
        i.join()

    for col in nMatriz:
        cadenaBytes = b''
        for fila in col:
            for valor in fila:
                cadenaBytes = cadenaBytes + bytes(valor)
        os.write(fd,cadenaBytes)
    #print(nMatriz)