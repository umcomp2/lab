from sys import getsizeof
import sys
import os
import stat
import multiprocessing as mp
from multiprocessing import Process, Queue
import argparse_1
global_path = argparse_1.path

def get_header():
    header = []
    fd = os.open(global_path, os.O_RDONLY)
    data = os.read(fd, 100)
    values = data.split()
    try:
        for i in values:
            i.decode()
            if len(header) <= 3:
                if i.isdigit() or i == b'P6':
                    header.append(i)
            else: 
                break
    except UnicodeDecodeError:
        pass
    magic_number = (header[0]).decode()
    alto = (header[1]).decode()
    ancho = (header[2]).decode()
    # The maximum color value (Maxval),
    # again in ASCII decimal. Must be less than 65536 and more than zero.
    maxval = (header[3]).decode()

    tamano_ruster = (int(header[1])*int(header[2]))*3
    tamano_archivo = os.stat(global_path).st_size
    tamano_header = (tamano_archivo-tamano_ruster)

    print('HEADER:\nMagic Number:{}\nAlto:{}\nAncho:{}\nMaxval:{}'.format(magic_number,
                                                                          alto,
                                                                          ancho,
                                                                          maxval))


    
    return [tamano_header, tamano_ruster, tamano_archivo]

# manipula archivito.txt   donde tengo mi ruster. 
def ruster(lista, archivito, nro):
    tamano_header = lista[0]
    tamano_ruster = lista[1]
    fd = os.open(global_path, os.O_RDWR)
    fd2 = os.open(archivito, os.O_RDWR | os.O_CREAT)
    # establecer puntero en comienzo del ruster
    data1 = os.read(fd, tamano_header)

    # comienzo ruster
    puntero = -1


    #mientras lee separa por colores
    while True:
        leido = os.read(fd, (nro))
        for i in leido: 
            puntero += 1
            if puntero % 3 == 0: 
                q_red.put(i)
            elif puntero % 3 == 1:
                q_green.put(i)
            elif puntero % 3 == 2:
                q_blue.put(i)
        #print("bloque de tamano: ", len(leido), "enviado")
        if len(leido) != nro:
            break   
    
    print("Bytes ruster: ", q_green.qsize() + q_green.qsize() + q_blue.qsize())


def get_red(q):

    red = open('red.txt', 'w')
    red.write(global_path)
    red.write("\nHISTOGRAMA RED\n")
    diccionario_rojo = {}
    for i in range(256):
        diccionario_rojo[i] = 0

    # habia hecho q.empty is False pero no anduvo, porque?? 
    while q.qsize() != 0: 
        rojo = q.get()
        diccionario_rojo[rojo] += 1

    values = 0
    for key, value in diccionario_rojo.items():
        red.write("valor: {} frecuencia: {}\n".format(key, value))
        values += value
    
    print('\nChequeando que la suma de frecuencias sean igual que la cantidad de pixeles: ', values, '\n')

    if q.qsize() == 0:
        print("red queue EMPTY")
    red.close()



def get_green(q):
    green = open('green.txt', 'w')
    green.write(global_path)
    green.write("\nHISTOGRAMA GREEN\n")
    diccionario_verde = {}
    for i in range(256):
        diccionario_verde[i] = 0  

    while q.qsize() != 0:  
        verde = q.get()
        diccionario_verde[verde] += 1
    
    values = 0
    for key, value in diccionario_verde.items():
        green.write("valor: {} frecuencia: {}\n".format(key, value))
        values += value

    print('\nChequeando que la suma de frecuencias sean igual que la cantidad de pixeles: ', values, '\n')    
    if q.qsize() == 0:
        print("green queue EMPTY")

    green.close()

def get_blue(q):
    blue= open('blue.txt', 'w')
    blue.write(global_path)
    blue.write("\nHISTOGRAMA BLUE\n")
    diccionario_azul = {}
    for i in range(256):
        diccionario_azul[i] = 0  

    while q.qsize() != 0: 
        azul = q.get()
        diccionario_azul[azul] += 1

    values = 0
    for key, value in diccionario_azul.items():
        blue.write("valor: {} frecuencia: {}\n".format(key, value))
        values += value
    
    print('\nChequeando que la suma de frecuencias sean igual que la cantidad de pixeles: ', values, '\n')

    if q.qsize() == 0:
        print("blue queue EMPTY")
    
    blue.close()

if __name__ == '__main__':

    print("\nRealizando histograma ", global_path, '\n')

    lista = get_header()
    archivito = 'archivito.txt'

    q_red = mp.Queue()
    q_green = mp.Queue()
    q_blue = mp.Queue()


    ruster(lista, archivito, argparse_1.numero)

    
    p1 = Process(target=get_red, args=(q_red,))
    p2 = Process(target=get_green, args=(q_green,))
    p3 = Process(target=get_blue, args=(q_blue,))

    print("tamano queue red: ", q_red.qsize())
    print("tamano queue green: ", q_green.qsize())
    print("tamano queue blue: ", q_blue.qsize())
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    os.remove(archivito)

    
    print("tamano queue red: ", q_red.qsize())
    print("tamano queue green: ", q_green.qsize())
    print("tamano queue: blue", q_blue.qsize())
