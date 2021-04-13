#!/usr/bin/python3
#este codigo SOLO hace la comunicacion entre proceso usando mensajes 
#hijo1 -> hijo2 SIGUSR1
#hijo2 -> hijo1 SIGUSR2
#hijo2 -> hijo1 SIGTERM
#hijo2 -> hijo2 SIGTERM
import os
import signal
import time

pidh1 = 0
pidh2 = 0

def modifyText(nro,frame):
    global pidh1
    linea = os.read(l12,1024).decode('utf-8')
    while linea != '':
        # procesar línea
        salida = rot13(linea)
        os.write(e21, salida.encode())
        linea = os.read(l12,1024).decode('utf-8')

    print ("hijo2 reemplazando ..")
    os.close(e21)
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

def showModified(nro,frame):
    print ("hijo1 leyendo .......")
    while True:
        leido = os.read(l21, 1024)
        os.write(1, leido)
        if len(leido) == 0:
            break
    os.close(l21)
    # suicidio en masa
    global pidh2
    os.kill(pidh2, signal.SIGTERM)
    os.kill(os.getpid(), signal.SIGTERM)


def finishSon(nro,frame):
    exit()

if __name__ == '__main__':
    l12,e12 = os.pipe()
    l21,e21 = os.pipe()
#
#      ------  e12      l12   ------   e21        l21  ------
#      | h1 | --------------> | h2 | ----------------> | h1 | 
#      ------                 ------                   ------
    pidh2 = os.fork()
    if pidh2 == 0: #hijo2
        signal.signal(signal.SIGUSR1, modifyText)
        signal.signal(signal.SIGTERM, finishSon)
        os.close(e12)
        os.close(l21)
        while True:
            time.sleep(10)
        exit()
        signal.pause()

    pidh1 = os.fork()
    if pidh1 == 0: #hijoh1
        signal.signal(signal.SIGUSR2, showModified)
        signal.signal(signal.SIGTERM, finishSon)
        os.close(l12)
        os.close(e21)
        print ("hijo1 escribiendo ...")
        while True:
            leido = os.read (0, 1024)
            os.write (e12, leido)
            if len(leido) == 0:
                break
        os.close(e12)
        os.kill(pidh2,signal.SIGUSR1) #le mando un SIGUSR1 a mi hermano, el hijo2
        signal.pause()

#padre 
    signal.signal(signal.SIGUSR2, signal.SIG_IGN)
    os.close(l12)
    os.close(e12)
    os.close(l21)
    os.close(e21)
    os.wait()
    os.wait()
    print ("terminaron todos los hijos")
