#!/usr/bin/python3
import os
import getopt
import sys

def main():
    n = 0
    m = 0
    c = 0
    try:
        opc, args = getopt.getopt(sys.argv[1:], "vhc:",["help"])
    except:
        print('Error al leer los argumentos, use el --help para desplegar la ayuda')
        sys.exit()
    for o, a in opc:
        if o in ("-h", "--help"):
           print('Ayuda: Los argumentos validos son -v (verboso) y -c (cantidad de hijos)')
           sys.exit()
        elif o == "-v":
            print('...Modo verboso...')
            print('Los argumentos ingresados son: ',opc)
        elif o in ("-c"):
            c = int(a)
        else:
            print('Argumento no valido, use -h o --help para un ayudin')

    if (c == 0):
        print('Faltan argumentos, use -h o --help para un ayudin')
        sys.exit()
    for i in range(c):
        hijo = os.fork()
        if hijo == 0:
            print("---------------------")

            n = input('Ingrese 1er numero: ')
            m = input('Ingrese 2do numero: ')

            print("-------------Creando hijo-------------\nPID hijo: {} \npromedio: {} \ncreado por PID: {}".format(os.getpid(), promedio(int(n),int(m)), os.getppid()))
            exit()
        else:
            print("--------Padre--------")
            print("PID padre {}".format(os.getpid()))
            os.wait()
            print("\nTermino el hijo\n")

def promedio(n, m):
    return (n+m)/2

if __name__ == '__main__':
    main()
