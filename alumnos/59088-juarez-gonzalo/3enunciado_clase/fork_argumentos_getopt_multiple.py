#!/usr/bin/env python3

import os
import sys
import argparse
import multiprocessing

def promedio(n, m):
    return (n + m) / 2

def reportar_padre(v):
    if v:
        sys.stdout.write("...Modo verboso...\nPID padre: %d\nCreando hijos\n" % os.getpid())
        sys.stdout.flush()

def reportar_hijo(p, v):
    out = ""

    if v:
        pid = os.getpid()
        out += "PID hijo: %d\n" % pid
        out += "promedio: %f creado por %d" % (p, pid)
    else:
        out += "%f" % p

    sys.stdout.write(out + "\n")
    sys.stdout.flush()

def usage():
    print("Usage: %s -c num_forks" % __file__)

def fc_hijo(lock, v):
    lock.acquire()

    n = float(input("Ingrese el 1er numero: "))
    m = float(input("Ingrese el 2do numero: "))
    r = promedio(n, m)
    reportar_hijo(r, v)

    lock.release()
    sys.exit(0)

def main():
    try:
        parser = argparse.ArgumentParser(description="Calculadora de multiples promedios")
        parser.add_argument("-c", "--cantidad", type=int, help="Cantidad de forks del proceso")
        parser.add_argument("-v", "--verboso", action="store_true", help="verboso")
        args = parser.parse_args()

        ppid = os.getpid()
        lock = multiprocessing.Lock()

        reportar_padre(args.verboso)

        for i in range(0, args.cantidad):
            pid = os.fork()
            if not pid:
                fc_hijo(lock, args.verboso)

        if os.getpid() == ppid:
            for i in range(0, args.cantidad):
                os.waitid(os.P_PGID, 0, os.WEXITED)

    except Exception as err:
        sys.stdout.write(str(err))
        usage()

if __name__ == "__main__":
    main()
