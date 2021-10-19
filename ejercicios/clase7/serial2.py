import threading
import time

saldo = 5

def transferencia(monto):
    print("Thread tranf: starting")
    global saldo
    time.sleep(0.1)
    saldo = saldo + monto
    print("termino el hilo de transferencia", saldo)

def extraer(monto):
    print("Thread extrae: starting")
    #dos segundo del hilo y
    global saldo
    while (saldo - monto) < 0:
        #print(".", end="")
        pass
    saldo = saldo - monto
    print("termino el jilo de extraccion", saldo)

if __name__=="__main__":
    x = threading.Thread(target=transferencia, args=(10000,))
    y = threading.Thread(target=extraer, args=(2000,))
    x.start()
    y.start()
    x.join()
    y.join()
    time.sleep(2)
    print(saldo)
    exit(0)




