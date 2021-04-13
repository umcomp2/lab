#!/usr/bin/python3
import os
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


if __name__ == '__main__':
    l12,e12 = os.pipe()
    l21,e21 = os.pipe()
#
#      ------  e12      l12   ------   e21        l21  ------
#      | h1 | --------------> | h2 | ----------------> | h1 | 
#      ------                 ------                   ------
    pidh2 = os.fork()
    if pidh2 == 0: #hijo2
        os.close(e12)
        os.close(l21)
        linea = os.read(l12,1024).decode('utf-8')
        while linea != '':
            # procesar línea
            salida = rot13(linea)
            os.write(e21, salida.encode())
            linea = os.read(l12,1024).decode('utf-8')
        print ("hijo2 reemplazando ..")
        os.close(e21)
        os._exit(os.EX_OK)

    pidh1 = os.fork()
    if pidh1 == 0: #hijoh1
        os.close(l12)
        os.close(e21)
        print ("hijo1 escribiendo ...")
        while True:
            leido = os.read (0, 1024)
            os.write (e12, leido)
            if len(leido) == 0:
                break
        os.close(e12)
        print ("hijo1 leyendo .......")
        while True:
            leido = os.read(l21, 1024)
            os.write(1, leido)
            if len(leido) == 0:
                break
        os.close(l21)
        exit(0)

#padre 
    os.close(l12)
    os.close(e12)
    os.close(l21)
    os.close(e21)
    os.wait()
    os.wait()
    print ("terminaron todos los hijos")
