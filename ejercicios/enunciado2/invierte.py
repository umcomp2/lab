#!/usr/bin/python3
import sys

a = sys.stdin.read()

def invertir(cod):
    return str(cod[::-1])

sys.stdout.write("Palabras invertidas: " + invertir(a))

