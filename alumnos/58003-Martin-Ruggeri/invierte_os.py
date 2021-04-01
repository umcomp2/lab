#!/usr/bin/python3
import os

def invierte_os():
    while True :
        leido = os.read(0, 1024)
        for renglon in leido.splitlines():
            for palabra in renglon.split():
                os.write(1,(palabra[::-1] + b" "))
            os.write(1, b"\n")
        if len(leido) != 1024:
            break


if __name__== '__main__':
    invierte_os()