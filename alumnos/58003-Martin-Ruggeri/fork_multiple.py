#!/usr/bin/python3
import argparse
import os
import sys


def constructorHijos(args):
    for i in range(args.c):
        hijo = os.fork()
        if hijo > 0:
            os.waitpid(hijo, 0)
            break
        if hijo == 0:
            n = float(input("ingrese primer valor"))
            m = float(input("ingrese primer valor"))
            resultado = 0.5 * (n + m)
            if args.verbose:
                modoVerbosoHijo(args, n, m, resultado)
            else:
                print(resultado)


def modoVerbosoHijo(args, n, m, resultado):
    print(f"\tPID del hijo: {os.getpid()}")
    print(
        f"\tEl promedio entre {m} y {n} es: {resultado}")
    print(f"\tMi padre es {os.getppid()}")
    print("\tTerminando hijo")


def modoVerbosoPadre(args):
    print("Modo verboso")
    pidPadre = os.getpid()
    print(f"PID del padre: {os.getpid()}")
    print("Creando hijos")
    constructorHijos(args)
    if pidPadre == os.getpid():
        print("Terminando el padre")
        sys.exit(0)


def parseador():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="descripcion del resultado")
    parser.add_argument("c", type=int, help="cantidad de hijos")
    return parser.parse_args()


def main():
    args = parseador()
    if args.verbose:
        modoVerbosoPadre(args)
    else:
        constructorHijos(args)
        sys.exit(0)


if __name__ == "__main__":
    main()
