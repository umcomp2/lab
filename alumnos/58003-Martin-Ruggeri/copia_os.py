#!/bin/python3
import os


def copiaArchivosOS():
    pad1 = input("ingrese archivo de origen:\n")
    pad2 = input("ingrese archivo de destino:\n")
    fdo = os.open(pad1, os.O_RDONLY)
    fdd = os.open(pad2, os.O_WRONLY | os.O_CREAT)
    while True:
        leido = os.read(fdo, 1024)
        os.write(fdd, leido)
        if len(leido) != 1024:
            break


if __name__ == '__main__':
    copiaArchivosOS()
