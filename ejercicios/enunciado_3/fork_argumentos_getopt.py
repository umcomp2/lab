#!/usr/bin/python3

import os
import getopt
import sys

def promedio(n,m):
    return (n+m)/2

def main():
    n = 0
    m = 0
    try:
        opciones, args = getopt.getopt(sys.argv[1:], "vn:m:h",["help"])
    except:
        print("Argumento errónero, ingrese --help")
        sys.exit()

    for o,a in opciones:
        if o in ("-h", "--help"):
            print("--- Los argumentos válidos son -v (verboso), -n (Nro1), -m (Nro2)")
            sys.exit()
        elif o == "-v":
            print("...Modo verboso.... \n Argumentos ingresados: ", opciones)
        elif o in ("-n"):
            n = int(a)
        elif o in ("-m"):
            m = int(a)
        else:
            print("Argumento no válido, use -h o --help")

    if (n==0 and m==0):
        print("No se creo el hijo por que no se puede sacar el promedio de 0, use -h o --help ")
        sys.exit()
    hijo = os.fork()
    if hijo == 0: #Seccion del hijo
        print("....Creando al hijo.... \n PID hijo: {} Promedio: {}  creado por PID: {}".format(os.getpid(), promedio(n,m), os.getpid()))
        sys.exit()
    else: #Seccion del padre
        print("PID padre {}".format(os.getpid()))


    
if __name__ == "__main__":
    main()
