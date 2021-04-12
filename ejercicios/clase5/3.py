#!/usr/bin/python3
import os
import multiprocessing
import time

def rot13(entrada):
    codec = "abcdefghijklmnopqrstuvwxyz"
    codec2 = codec + codec
    salida = ""
    for caracter in entrada:
        indice = (codec.find(caracter))
        if indice >= 0:
            salida = salida + codec2[indice+13]
        else :
            salida = salida + caracter
    return (salida)

def h1(h1pipe):
    print ("hijo1 escribiendo ...")
    while True:
        leido = os.read (0, 1024)
        h1pipe.send(leido)
        if leido == b'':
            break
    print ("hijo1 leyendo .......")
    leido = h1pipe.recv()
    while leido != b'EOF':
        os.write(1, leido)
        leido = h1pipe.recv()

def h2(h2pipe):
    print ("hijo2 reemplazando ..")
    linea = h2pipe.recv().decode('utf-8')
    while linea != '':
        # procesar línea
        salida = rot13(linea)
        h2pipe.send(salida.encode())
        linea = h2pipe.recv().decode('utf-8')
    h2pipe.send(b'EOF')

if __name__ == '__main__':

    h1pipe,h2pipe = multiprocessing.Pipe()
#
#      ------ h112      h212  ------  h221        h121 ------
#      | h1 | --------------> | h2 | ----------------> | h1 | 
#      ------                 ------                   ------
    ph1 = multiprocessing.Process(target=h1, args=(h1pipe,))
    ph2 = multiprocessing.Process(target=h2, args=(h2pipe,))

    ph1.start()
    ph2.start()

    ph1.join()
    ph2.join()

    print ("terminaron todos los hijos")
