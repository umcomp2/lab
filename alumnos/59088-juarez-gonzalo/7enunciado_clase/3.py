#!/usr/bin/env python3
import threading

acc = 0
sem = None

def suma(num):
    global acc
    global sem

    print("Saldo = %d, Sumando =  %d" % (acc, num))
    acc += num
    sem.release()

def resta(num):
    global acc
    global sem

    sem.acquire()
    print("Saldo = %d, Restando =  %d" % (acc, num))
    acc -= num

if __name__ == "__main__":
    dep = 1000
    extrac = 500

    pool = []
    sem = threading.Semaphore(value=0)

    pool.append(threading.Thread(target=suma, args=(dep,)))
    pool.append(threading.Thread(target=resta, args=(extrac,)))

    for t in pool:
        t.start()

    for t in pool:
        t.join()

    print("Acumulador final %d" % acc)
