#!/usr/bin/python3

import os
import getopt
import sys

def promedio(n,m):
    return (n+m)/2

def main():
    n = 2
    m = 0
    c = 0
    try:
        opciones, args = getopt.getopt(sys.argv[1:], "vhc:",["help"])
    except:
        print("Argumento errónero, ingrese --help")
        sys.exit()

    for o,a in opciones:
        if o in ("-h", "--help"):
            print("--- Los argumentos válidos son -v (verboso), -c(cantidad de hijos)")
            sys.exit()
        elif o == "-v":
            print("...Modo verboso.... \n Argumentos ingresados: ", opciones)
        elif o in ("-c"):
            c = int(a)
        else:
            print("Argumento no válido, use -h o --help")

    if (c == 0):
        print("Faltan argumentos, use -h o --help ")
        sys.exit()

    for i in range(c):
        hijo = os.fork()
        if hijo == 0: #Seccion del hijo
            n = input("Ingrese un numero: ")
            m = input("Ingrese el segundo número: ")
            print("....Creando al hijo.... \n PID hijo: {} Promedio: {}  creado por PID: {}".format(os.getpid(), promedio(int(n),int(m)), os.getpid()))
            sys.exit()
        else: #Seccion del padre
            os.wait()
            print("Terminó el hijo: ")
    print("Terminó el padre: ")
    print("PID padre {}".format(os.getpid()))


    
if __name__ == "__main__":
    main()
