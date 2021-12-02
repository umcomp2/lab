#!/usr/bin/python3
import argparse

pars = argparse.ArgumentParser(description='Calculadora')

group = pars.add_mutually_exclusive_group(required=True)
group.add_argument('-s', '--suma',action="store_true", help="suma arg1 + arg2")
group.add_argument('-r', '--resta',action="store_true", help="resta arg1 + arg2")
group.add_argument('-m', '--multiplicacion',action="store_true", help="multiplicar arg1 * arg2")
group.add_argument('-d', '--division',action="store_true", help="divide arg1 / arg2 ")
#Argumento para el tipo de numero
pars.add_argument('-t', '--type', choices=["int","float"], default="int", help="tipo de numero[int|float]")
#Argumento de los numeros de la operacion
pars.add_argument('numeros', type=float, nargs=2, help='Numeros para la operacion')

args =  pars.parse_args()

print (args)
if args.type == "int":
    op1 = int(args.numeros[0])
    op2 = int(args.numeros[1])
elif args.type == "float":
    op1 = float(args.numeros[0])
    op2 = float(args.numeros[1])
else:
    print ("type invalido")
    exit(0)

if args.suma == True:
    print (op1 + op2)
elif args.resta == True:
    print (op1 - op2)
elif args.multiplicacion == True:
    print (op1 * op2)
elif args.division == True:
    print (op1 / op2)
