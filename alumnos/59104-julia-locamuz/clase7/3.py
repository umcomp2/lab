import threading
import time

saldo = 5 
#barrier = threading.Barrier(2)

def transferencia(monto):
    print("Thread transf: starting")
    global saldo
    saldo = saldo + monto 
    print("termino el hilo transferencia", saldo)

def extrae(monto): 
    print("Thread extrae: starting")
    global saldo
    x.join()
    saldo = saldo - monto
    print("termino el hilo extraccion", saldo)

if __name__ == '__main__':
    x = threading.Thread(target=transferencia, args=(10000,))
    y = threading.Thread(target=extrae, args=(2000,))
    x.start()
    y.start()
    #x.join()
    y.join()
    print(saldo)
