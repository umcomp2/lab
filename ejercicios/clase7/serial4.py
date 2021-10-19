import threading
import time

saldo = 5

sem = threading.Semaphore(0)

def transferencia(monto):
    print("Thread tranf: starting")
    global saldo
    time.sleep(3)
    saldo = saldo + monto
    sem.release()
    print("termino el hilo de transferencia", saldo)

def extraer(monto):
    print("Thread extrae: starting")
    #dos segundo del hilo y
    global saldo
    sem.acquire()
    saldo = saldo - monto
    print("termino el jilo de extraccion", saldo)

if __name__=="__main__":
    x = threading.Thread(target=transferencia, args=(10000,))
    y = threading.Thread(target=extraer, args=(2000,))
    x.start()
    y.start()
    x.join()
    y.join()
    print(saldo)
    exit(0)




