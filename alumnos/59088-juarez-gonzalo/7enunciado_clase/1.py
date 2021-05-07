#!/usr/bin/env python3
import threading

def printmsg():
    print("ejecutando...")

if __name__ == "__main__":
    pool = []
    nthreads = 2

    for i in range(nthreads):
        pool.append(threading.Thread(target=printmsg))
        pool[-1].start()

    for t in pool:
        t.join()
