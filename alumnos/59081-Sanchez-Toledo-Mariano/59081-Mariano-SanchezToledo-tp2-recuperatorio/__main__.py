from os import O_CREAT
from matriz import *
from threading import Thread, ThreadError
from queues import *
from common import *


def main():
    
    rq = Queue()
    gq = Queue()
    bq = Queue()

    thQueue = Thread(target=processQueue, name='ThQueue', args=(rq, gq, bq,))
    th1 = Thread(target=llenar_matriz_rojo, name='rojo', args=(rq,))
    th2 = Thread(target=llenar_matriz_verde, name='verde', args=(gq,))
    th3 = Thread(target=llenar_matriz_azul, name='azul', args=(bq,))

    thQueue.start()
    th1.start()
    th2.start()
    th3.start()

    thQueue.join()
    th1.join()
    th2.join()
    th3.join()

    espejo = invertirMatriz()

    with open('espejo.ppm', 'wb', O_CREAT) as fd:
        fd.write(header)
        for y in range(len(espejo)):
            for x in range(len(espejo[y])):
                for k in espejo[y][x]:
                    fd.write(k)


if __name__ == "__main__":
    main()