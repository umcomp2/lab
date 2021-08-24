import threading
import time

saldo = 5

barrera = threading.Barrier(3)

def transferencia(monto):
    print("Thread tranf: starting")
    global saldo
    #time.sleep(5)
    saldo = saldo + monto
    #punto de encuentro
    barrera.wait()
    print("Saldo final", saldo)
    time.sleep(1)
    print("hilo de transferencia sigue trabajando")

def extraer(monto):
    print("Thread extrae: starting")
    #dos segundo del hilo y
    global saldo
    saldo = saldo - monto
    #Punto de encuentro
    barrera.wait()
    print("saldo final", saldo)
    time.sleep(2)
    print("hilo extrae sigue trabajando")

def hb(monto):
    print("Thread hb: starting")
    #dos segundo del hilo y
    time.sleep(2)
    global saldo
    saldo = saldo - monto
    #Punto de encuentro
    barrera.wait()
    print("saldo final", saldo)
    time.sleep(2)
    print("hilo hb sigue trabajando")

if __name__=="__main__":
    x = threading.Thread(target=transferencia, args=(10000,))
    y = threading.Thread(target=extraer, args=(2000,))
    z = threading.Thread(target=hb, args=(1500,))
    x.start()
    y.start()
    z.start()
    x.join()
    y.join()
    z.join()
    time.sleep(2)
    print(saldo)
    exit(0)