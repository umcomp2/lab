#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description="Calculadora Python")
#Grupo mutuamente excluyente(solo puede estar seleccioando uno)
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("-s", "--suma", action="store_true", help="Suma arg1 + arg2")
group.add_argument("-r", "--resta", action="store_true", help="Resta arg1 - arg2")
group.add_argument("-m", "--multiplicacion", action="store_true", help="Multiplica arg1 * arg2")
group.add_argument("-d", "--division", action="store_true", help="Divide  arg1 /  arg2")
#Revisar opcion de add_aergument
parser.add_argument("-t","--type", action="store", dest="type",metavar='type', type=str, choices=["int","float","real"], default="int", help="tipo de nros [int|float|real] - int default")
parser.add_argument("numeros", type=float, nargs=2, help="Numeros para la operacion", metavar="nro")

args = parser.parse_args()
#Para ver todas las variables de la clase
print(args)
if args.type == "int":
    op1 = int(args.numeros[0])
    op2 = int(args.numeros[1])
elif args.type == "float":
    op1 = int(args.numeros[0])
    op2 = int(args.numeros[1])
elif args.type == "real":
    op1 = int(args.numeros[0])
    op2 = int(args.numeros[1])
else:
    print("Type inválido")
    exit(0)
if args.suma == True:
    print(op1 + op2)
elif args.resta == True:
    print(op1 - op2)
elif args.multiplicacion == True:
    print(op1*op2)
elif args.division == True:
    print(op1 / op2)





