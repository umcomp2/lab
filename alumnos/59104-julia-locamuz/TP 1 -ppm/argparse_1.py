import argparse


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('file', help='file')
parser.add_argument('nro', type=int, help='nro bytes a leer')
parser.add_argument('-f',help='funcion file', action='store_true')
parser.add_argument('-n',help='funcion nro bytes a leer', action='store_true')
args = parser.parse_args()
if args.f: 
    path = args.file
if args.n: 
    numero = args.nro