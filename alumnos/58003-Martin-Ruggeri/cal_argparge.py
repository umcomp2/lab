#!/bin/python3
import argparse


parser = argparse.ArgumentParser(
    description='Calculadora, suma/resta/multiplicacion/division entre a y b')
parser.add_argument('-a', '--numero_a', type=int, help='Parámetro a')
parser.add_argument('-b', '--numero_b', type=int, help='Parámetro b')
parser.add_argument('-o', '--operacion', type=str,
                    choices=['suma', 'resta', 'multi', 'divi'],
                    default=max, required=False,
                    help='Las op para a y b son [suma, resta, multi, divi]')
args = parser.parse_args()

if args.operacion == 'suma':
    print(args.numero_a + args.numero_b)
elif args.operacion == 'resta':
    print(args.numero_a - args.numero_b)
elif args.operacion == 'multi':
    print(args.numero_a * args.numero_b)
elif args.operacion == 'divi':
    print(args.numero_a / args.numero_b)
