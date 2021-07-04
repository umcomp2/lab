#!/usr/bin/python3
import os
print("Ingrese una palabra: ")
a = os.read(0,20)
print("Su palabra se invertirá")
os.write(1,a[::-1])
print ("\n")
