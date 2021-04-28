#!/usr/bin/python3
#este codigo SOLO hace la comunicacion entre proceso usando mensajes 
#hijo1 -> hijo2 SIGUSR1
#hijo2 -> hijo1 SIGUSR2
#hijo2 -> hijo1 SIGTERM
#hijo2 -> hijo2 SIGTERM
import os
import argparse
import signal
import time

pidh1 = 0
pidh2 = 0

def modifica_archivo(nro,frame):
    global pidh1
    archivo = open("archivo.txt",'r')
    salida = ''
    linea = archivo.readline()
    while linea != '':
        # procesar línea
        salida = salida + rot13(linea)
        linea = archivo.readline()
    archivo.close()
    print ("hijo2 reemplazando ..")
    archivo = open("archivo.txt",'w')
    archivo.write(salida)
    archivo.close()
    os.kill(pidh1, signal.SIGUSR2)

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

def muestra_modificado(nro,frame):
    print ("hijo1 leyendo .......")
    fd = os.open("archivo.txt",os.O_RDONLY)
    while True:
        leido = os.read(fd, 1024)
        os.write(1, leido)
        if len(leido) == 0:
            break
    os.close(fd)
    # suicidio en masa
    global pidh2
    os.kill(pidh2, signal.SIGTERM)
    os.kill(os.getpid(), signal.SIGTERM)


def termina_hijo(nro,frame):
    exit()

if __name__ == '__main__':

    pidh2 = os.fork()
    if pidh2 == 0: #hijo2
        signal.signal(signal.SIGUSR1, modifica_archivo)
        signal.signal(signal.SIGTERM, termina_hijo)
        #while True:
        #    time.sleep(10)
        #exit()
        #Wait until a signal arrives.
        signal.pause()

    pidh1 = os.fork()
    if pidh1 == 0: #hijoh1
        signal.signal(signal.SIGUSR2, muestra_modificado)
        signal.signal(signal.SIGTERM, termina_hijo)
        fd = os.open("archivo.txt",os.O_CREAT|os.O_WRONLY|os.O_TRUNC, 440)
        print ("hijo1 escribiendo ...")
        while True:
            leido = os.read (0, 1024)
            os.write (fd, leido)
            if len(leido) == 0:
                break
        os.close(fd)
        os.kill(pidh2,signal.SIGUSR1) #le mando un SIGUSR1 a mi hermano, el hijo2
        #while True:
        #    time.sleep(10)
        #exit()
        #Wait until a signal arrives.
        signal.pause()

#padre 
    signal.signal(signal.SIGUSR2, signal.SIG_IGN)
    os.wait()
    os.wait()
    print ("terminaron todos los hijos")
