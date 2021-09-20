#!/usr/bin/python3
import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="descripcion del resultado")
    parser.add_argument("x", type=float, help="1er numero")
    parser.add_argument("y", type=float, help="2do numero")
    args = parser.parse_args()

    if args.verbose:
        print("Modo verboso")
        print(f"PID del padre: {os.getpid()}")
        print("Creando hijo")
    hijo = os.fork()
    print(hijo)
    print(f"soy {os.getpid()}")

    if hijo > 0:
        os.waitpid(hijo, 0)
        if args.verbose:
            print("Terminando el padre")
        sys.exit(0)
    elif hijo == 0:
        resultado = 0.5 * (args.x + args.y)
        if args.verbose:
            print(f"\tPID del hijo: {os.getpid()}")
            print(f"\tEl promedio entre {args.x} y {args.y} es: {resultado}")
            print(f"\tMi padre es {os.getppid()}")
            print("\tTerminando hijo")
        else:
            print(resultado)
        sys.exit(0)


if __name__ == "__main__":
    main()
