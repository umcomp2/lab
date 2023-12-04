#!/usr/bin/python3

import os


print("Ingrese una palabra: ")

letras = os.read(0,30)

print("Su palabra invertida es: ")  
        
os.write(1,letras[::-1])

print("\n")


