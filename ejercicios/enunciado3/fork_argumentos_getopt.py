#!/usr/bin/python3 
import os
import getopt
import sys

def main():
    n = 0
    m = 0
    try:
        opciones, args = getopt.getopt(sys.argv[1:], "vn:m:h",["help"])
    except:
        print('No se pudieron leer los argumentos, use el --help para desplegar la ayuda')
        sys.exit()
    for o, a in opciones:
        if o in ("-h", "--help"):
           ayuda()
           sys.exit()
        elif o == "-v":
            print('-------Modo verboso--------\nLos argumentos ingresados son: ',opciones)
        elif o in ("-n"):
            n = int(a)
        elif o in ("-m"):
            m = int(a)
        else:
            print('Argumento no valido, use -h o --help para desplegar la ayuda')
        
    if (n==0 or m==0):
        print('No se creo hijo, use -h o --help para un ayudin')
        sys.exit()
    hijo_pid = os.fork()
    if hijo_pid == 0: #Hijo
        print("-------------Creando hijo-------------\nPID hijo: {} \npromedio: {} \ncreado por PID: {}".format(os.getpid(), promedio(n,m), os.getppid()))
        sys.exit()
    else:
        print("--------Padre--------")
        print("PID padre {}".format(os.getpid()))

def promedio(n, m):
    return (n+m)/2

def ayuda():
    print("Ayuda: Los argumentos validos son -v (verboso) -n (base) -m (exponente)")


if __name__ == '__main__':
    main()
