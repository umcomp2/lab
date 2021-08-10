#!/usr/bin/env python3
import threading

acc = 0
acc_sem = None
barrier = None

def suma(num):
    global acc
    global acc_sem
    global barrier

    print("Saldo = %d, Sumando =  %d" % (acc, num))
    acc += num
    acc_sem.release()

    barrier.wait()
    print("Acumulador final %d, %d" % (acc, threading.get_native_id()))

def resta(num):
    global acc
    global acc_sem
    global barrier

    acc_sem.acquire()
    print("Saldo = %d, Restando =  %d" % (acc, num))
    acc -= num

    barrier.wait()
    print("Acumulador final %d, %d" % (acc, threading.get_native_id()))

if __name__ == "__main__":
    dep = 1000
    extrac = 500

    pool = []
    acc_sem = threading.Semaphore(value=0)
    barrier = threading.Barrier(2)

    pool.append(threading.Thread(target=suma, args=(dep,)))
    pool.append(threading.Thread(target=resta, args=(extrac,)))

    for t in pool:
        t.start()

    for t in pool:
        t.join()

    if acc < 0:
        raise ValueError("Acumulador negativo")
