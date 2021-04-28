#!/usr/bin/python3
import os
import getopt
import sys

def promedio(n, m):
    return (n+m)/2

if __name__ == '__main__':
    n,m,c = 2,0,0
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "vhc:",["help"])
    except:
        print('Error al leer los argumentos, use el --help para desplegar la ayuda')
        sys.exit()
    for o, a in optlist:
        if o in ("-h", "--help"):
           print('Ayuda: Los argumentos validos son -v (verboso) -h ayuda -c cantidad de hijos')
           sys.exit()
        elif o == "-v":
            print('...Modo verboso...')
            print('Argumentos ingresados: ',optlist)
        elif o in ("-c"):
            c = int(a)
        else:
            print('Argumento no valido, use -h o --help para desplegar la ayuda')
    #si no hay hijos que crear, termino
    if (c == 0):
        print('Faltan argumentos, use -h o --help para desplegar la ayuda')
        sys.exit()
    for i in range(c):
        hijo = os.fork()
        if hijo == 0:
            #seccion del hijo
            n = input('Ingrese 1er numero: ')
            m = input('Ingrese 2do numero: ')
            print("PID hijo: {} promedio: {} creado por: {}".format(os.getpid(), promedio(int(n),int(m)), os.getppid()))
            exit()
        else:
            #seccion del padre
            os.wait()
            print("Termino el hijo")
    print("Termino el padre")
    print("PID padre {}".format(os.getpid()))
