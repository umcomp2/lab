#!/bin/python3
import argparse


parser = argparse.ArgumentParser(
    description='Calculadora, suma/resta/multiplicacion/division entre a y b')
parser.add_argument('-a', '--numero_a', type=int, help='Parámetro a')
parser.add_argument('-b', '--numero_b', type=int, help='Parámetro b')
parser.add_argument('-o', '--operacion', type=str,
                    choices=['suma', 'resta', 'multiplicacion', 'division'],
                    default=max, required=False,
                    help='Operación a realizar con a y b')
args = parser.parse_args()

if args.operacion == 'suma':
    print(args.numero_a + args.numero_b)
elif args.operacion == 'resta':
    print(args.numero_a - args.numero_b)
elif args.operacion == 'multiplicacion':
    print(args.numero_a * args.numero_b)
elif args.operacion == 'division':
    print(args.numero_a / args.numero_b)
