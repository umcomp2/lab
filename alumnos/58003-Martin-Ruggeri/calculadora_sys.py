#!/bin/python3
import sys


if len(sys.argv) == 4 and sys.argv[1].isdigit and sys.argv[3].isdigit:
    if sys.argv[2] == "s":
        print(int(sys.argv[1]) + int(sys.argv[3]))
    elif sys.argv[2] == "r":
        print(int(sys.argv[1]) - int(sys.argv[3]))
    elif sys.argv[2] == "m":
        print(int(sys.argv[1]) * int(sys.argv[3]))
    elif sys.argv[2] == "d":
        print(int(sys.argv[1]) / int(sys.argv[3]))
    elif sys.argv[2] == "p":
        print(int(sys.argv[1]) ** int(sys.argv[3]))
    else:
        print(f"Error: uso {sys.argv[0]} nro [s, r, m, d, p] nro")
else:
    print(f"Error: uso {sys.argv[0]} nro [s, r, m, d, p] nro")
sys.exit()
