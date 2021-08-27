import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', help='file')
parser.add_argument('-f',help='funcion file', action='store_true')
args = parser.parse_args()
if args.f: 
    file = args.file
