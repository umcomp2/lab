#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('nro1', type=int, help='nro posicion 1')
parser.add_argument('nro2', type=int, help='nro posicion 2')
parser.add_argument('-s',help='suma', action='store_true')
parser.add_argument('-r',help='resta', action='store_true')
parser.add_argument('-m', help='multiplicacion', action='store_true')
parser.add_argument('-d', help='division', action='store_true')

args = parser.parse_args()

print(args.nro1)
print(args.nro2)

def main():
    try:
        if args.s: 
            print('suma is turned on')
            print(int(args.nro1) + int(args.nro2))


        if args.r: 
            print('resta is turned on')
            print(int(args.nro1) - int(args.nro2))


        if args.m: 
            print('multiplicacion is turned on')
            print(int(args.nro1) * int(args.nro2))


        if args.d: 
            print('division is turned on')
            print(int(args.nro1) / int(args.nro2))

    except Exception as exx: 
        print("argumentos no validos")
        print(exx)


if __name__ == '__main__':
    main()
