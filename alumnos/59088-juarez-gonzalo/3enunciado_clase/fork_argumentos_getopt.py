#!/usr/bin/env python3

import os
import argparse
import sys

def promedio(n, m):
    return (n + m) / 2

def reportar_padre(v):
    if v:
        sys.stdout.write("...Modo verboso...\nPID padre: %d\nCreando hijo\n" % os.getpid())
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
    print("Usage: %s [-v|--verboso] -n nro1 -m nro2" % __file__)

def main():
    try:
        parser = argparse.ArgumentParser(description="Calculadora de promedio entre 2 números")
        parser.add_argument("-v", "--verboso", action="store_true", help="verboso")
        parser.add_argument("-n", type=float, help="1er numero")
        parser.add_argument("-m", type=float, help="2do numero")
        args = parser.parse_args()

        reportar_padre(args.verboso)

        if not os.fork():
            r = promedio(args.n, args.m)
            reportar_hijo(r, args.verboso)
            sys.exit(0)
        else:
            os.wait()
    except Exception as err:
        usage()

if __name__ == "__main__":
    main()
