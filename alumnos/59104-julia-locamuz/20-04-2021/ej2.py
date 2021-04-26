from multiprocessing import Process, Pipe
import multiprocessing
import os
import argparse
import math
import sys


def enviar_pipe(humano, leido):
    print("\nENVIANDO INFORMACION DEL PIPE...")
    humano.send(leido)

def recibir_pipe(humano):
    print("\nRECIBIENDO INFORMACION DEL PIPE ")
    s = humano.recv()
    if s == b'':
        sys.exit()
    print(s, type(s), type(humano))

def cantidad_bloques(path, numOfBytes):
    stat = os.stat(path).st_size
    if stat % numOfBytes == 0: 
        bloques = stat / numOfBytes
    else: 
        bloques = math.ceil(stat/ numOfBytes)
    return bloques

if __name__ == '__main__':

    import argparse_ej2

    path = argparse_ej2.path
    numOfBytes = argparse_ej2.numero

    padre, hijo = Pipe()
    ph1 = Process(target=recibir_pipe, args=(hijo,))

    fd = os.open(path, os.O_RDONLY)

    bloques = cantidad_bloques(path, numOfBytes)

    ph1.start()
    #print(multiprocessing.active_children())
    bandera = True
    try:
        while bandera: 
            leido = os.read(fd, numOfBytes)
            enviar_pipe(padre, leido)
            if len(leido) == 0:
                print('El pipe esta vacio ya no hay informacion que enviar')
                sys.exit()
                break
            print("bloque de ", len(leido),"enviado al pipe")
            print(recibir_pipe(hijo))
            if ph1.is_alive() is False:
                bandera = False
        ph1.join()
    except EOFError as e:
        print(e.__str__)
        padre.close()
        hijo.close() 
    finally: 
        print("termino el programa")
        ph1.terminate()
        padre.close()
        hijo.close()