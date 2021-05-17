import threading
import queue
import time
def depositar(saldo,cola):
    depositado = int(input("Ingrese el saldo a depositar: "))
    saldo_actual = saldo + depositado
    cola.put(saldo_actual)
    print("Hilo 1 depositando {} -----> {}".format(depositado,saldo_actual))
    time.sleep(1)
    print("Su saldo actual es: ", saldo_actual)



def extraer(cola):
    extraer = int(input("Cuanto dinero quiere retirar:"))
    total = cola.get()
    saldo_actual = total - extraer
    print("Hilo 2 extrayendo {} -----> {}".format(extraer, saldo_actual))
    time.sleep(1)
    print("Su saldo actual es:", saldo_actual)
    
    
if __name__=='__main__':
    hilos = []
    saldo = 100
    q = queue.Queue()
    
    t1 = threading.Thread(target=depositar, args=(saldo, q, ))
    hilos.append(t1)
    t2 = threading.Thread(target=extraer, args=(q, ))
    hilos.append(t2)
    for hilo in hilos:
        hilo.start()
        hilo.join()

