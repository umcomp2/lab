import threading
import time

saldo = 5

sem = threading.Semaphore(0)
sem2 = threading.Semaphore(0)

def transferencia(monto):
    print("Thread tranf: starting")
    global saldo
    saldo = saldo + monto
    #punto de encuentro
    sem.release() #incrementa
    sem2.acquire() #decrementa
    print("Saldo final", saldo)
    time.sleep(1)
    print("hilo de transferencia sigue trabajando")

def extraer(monto):
    print("Thread extrae: starting")
    #dos segundo del hilo y
    time.sleep(5)
    global saldo
    saldo = saldo - monto
    #Punto de encuentro
    sem.acquire()
    sem2.release()
    print("saldo final", saldo)
    time.sleep(2)
    print("hilo extrae sigue trabajando")

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




