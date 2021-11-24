from concurrent.futures import ThreadPoolExecutor
import threading
import time


total = 100
s = threading.Semaphore(0)
s2 = threading.Semaphore(0)

def extraer(monto, n):
    global total
    total -= monto
    s.acquire
    s2.release()
    time.sleep(2)
    return f'hilo{n} extrayendo {monto}'

def depositar(monto, n):
    global total
    total += monto
    s.release()
    s2.acquire()
    time.sleep(1)
    return f'hilo{n} extrayendo {monto}'
    

if __name__=='__main__':
    print(total)
    with ThreadPoolExecutor(max_workers=2) as executor:
        t1 = executor.submit(depositar, 1000, 1)
        t2 = executor.submit(extraer, 500, 2)
        print(t1.result())
        print(t2.result())
    print('Terminaron los hilos')
    time.sleep(2)
    print('Saldo', total)
    exit(0)
