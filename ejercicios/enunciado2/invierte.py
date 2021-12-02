#!/usr/bin/python3
import sys

a = sys.stdin.read()

def invertir(cod):
    for j in cod.splitlines():
        for i in j.split():
            sys.stdout.write(i[::-1] + " ")
    sys.stdout.write("\n")

def main():
    var = invertir(a)

if __name__ == '__main__':
    main()
