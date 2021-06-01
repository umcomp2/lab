#!/usr/bin/python3 
import os
import getopt
import sys

def promedio(n, m):
    return (n+m)/2

if __name__ == '__main__':
    n,m = 0,0
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "vn:m:h",["help"])
    except:
        print('No se pudieron leer los argumentos, use el --help para desplegar la ayuda')
        sys.exit()
    for o, a in optlist:
        if o in ("-h", "--help"):
           print('Ayuda: Los argumentos validos son -v (verboso) -n (1er numero) -m (2do numero)')
           sys.exit()
        elif o == "-v":
            print('...Modo verboso...\nArgumentos ingresados: ',optlist)
        elif o in ("-n"):
            n = int(a)
        elif o in ("-m"):
            m = int(a)
        else:
            print('Argumento no valido, use -h o --help para desplegar la ayuda')

    if (n==0 or m==0):
        print('No se creo hijo porque falta uno o mas argumentos para el promedio, use -h o --help para desplegar la ayuda')
        sys.exit()
    hijo = os.fork()
    if hijo == 0: #seccion del hijo
        print("Creando hijo\nPID hijo: {} promedio: {} creado por PID: {}".format(os.getpid(), promedio(n,m), os.getppid()))
        sys.exit()
    else: #seccion del padre
        print("PID padre {}".format(os.getpid()))
