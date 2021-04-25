
from multiprocessing import Process, Pipe
import os


def pipe(humano, data):
    humano.send(data)
    humano.close()

if __name__ == '__main__':

    padre, hijo = Pipe()
    ph1 = Process(target=pipe, args=(hijo,['tomate', 22, 'manzana'],))
    #print(ph1.pid) # None , pq todavia no lo inicializo
    #ph1.start()
    #print(ph1.pid)
    ph1.start()
    ph2 = Process(target=pipe,args=(hijo,['conejo', 22, 'manzana'],))
    ph3 = Process(target=pipe, args=(hijo,['tomate', 65, 'Juan'],))
    print(padre.recv())
    ph1.join()

    ph2.start()
    print(padre.recv())
    