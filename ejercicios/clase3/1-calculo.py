#!/usr/bin/python3
import argparse

parser = argparse.ArgumentParser(description='Calculadora pyton')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-s', '--suma',action="store_true", default=False, help="Suma dos numeros")
group.add_argument('-r', '--resta',action="store_true", default=False, help="Resta dos numeros")
group.add_argument('-m', '--multi',action="store_true", default=False, help="Multi dos numeros")
group.add_argument('-d', '--divi',action="store_true", default=False, help="Divi dos numeros")
#revisar opcion choice de add_argument
parser.add_argument('-t', '--type',action="store", dest="type",metavar='type', type=str, choices=["int","float","real"], default="int", help="tipo de nros [int|float|real] - int default")
parser.add_argument('numeros', type=float, nargs=2, help='Numeros para la operacion',metavar='nro')

#(divi=False, multi=False, numeros=[1.0, 4.0], resta=False, suma=True, type=None)
args =  parser.parse_args()
#para ver todas las variables de la clase
print (args)
if args.type == "int":
    op1 = int(args.numeros[0])
    op2 = int(args.numeros[1])
elif args.type == "float":
    op1 = args.numeros[0]
    op2 = args.numeros[1]
elif args.type == "real":
    #deprecated para python3
    #op1 = long(args.numeros[0])
    op1 = args.numeros[0]
    #deprecated para python3
    #op2 = long(args.numeros[1])
    op2 = args.numeros[1]
#este else no tiene mucho sentido ... 
else:
    print ("type invalido")
    exit(0)
if args.suma == True:
    print (op1 + op2)
elif args.resta == True:
    print (op1 - op2)
elif args.multi == True:
    print (op1 * op2)
elif args.divi == True:
    print (op1 / op2)
