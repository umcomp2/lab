import argparse


parser = argparse.ArgumentParser(description='Cantidad de hijos')
parser.add_argument('n', type=int, help='Cant nro hijos')
args = parser.parse_args()