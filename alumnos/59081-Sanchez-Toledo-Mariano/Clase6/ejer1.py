#!/bin/python3

import argparse
import os


def leer(fd):
    header = []
    fd = os.open(fd, os.O_RDONLY)
    data = os.read(fd, 100).split()
    for i in data:
        if i == b'P6':
            header.append(i)
        elif i == b'#':
            header.append(i)
        elif i.isdigit():
            header.append(i)
        else:
            pass
    print(header)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extraer header de ppm')
    parser.add_argument('-f', '--file', type=str, help='Ingrese ruta de archivo ppm')
    args = parser.parse_args()

    leer(args.file)
