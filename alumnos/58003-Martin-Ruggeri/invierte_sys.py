#!/bin/python3
import sys
def invierte_sys():
    while True :
        leido = sys.stdin.read()
        for renglon in leido.splitlines():
            for palabra in renglon.split():
                sys.stdout.write(palabra[::-1] + " ")
            sys.stdout.write("\n")
        if len(leido) != 1024:
            break

if __name__== '__main__':
    invierte_sys()