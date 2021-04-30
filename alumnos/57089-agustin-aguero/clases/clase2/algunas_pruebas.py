#!/usr/bin/python3
import sys
import getopt

#print(sys.argv)     #esto devuelve un ['algunas_pruebas.py'] , si lo corriese con "./" daria ['./algunas_pruebas.py']
                    #tambien si le escribo en terminal: python3 ./algunas_pruebas.py 123 hola como estas "hola como estas" 3
                    # devuelve un ['./algunas_pruebas.py', '123', 'hola', 'como', 'estas', 'hola como estas' , '3']
#si corro las sig dos linea con: python3 ./algunas_pruebas.py 123 hola como estas "hola como estas" 3
#print(sys.argv[1]+sys.argv[6])             # 1233
#print(int(sys.argv[1])+int(sys.argv[6]))   # 126

args = sys.argv[1:]   # esto va a guardar en una variable los argumentos de entrada omitiendo la posicion cero que sera el nombre del archivo .py que estamos usando
print(f"entrada:\n{args}")
ayuda = "hola"

opciones , args = getopt.getopt(args, "srmdph") #aca creare una variable opciones que tomara como parametro una lista de argumentos que empiecen con "-"
print(f"argumentos:\n{args}")                   #los argumentos que tomo opciones se los saco a args y lo dejo con lo que quedaba
print(f"opciones:\n{opciones}")
for elementos in args:
    if elementos.isdigit() != True:
        print("los argumentos a operar no son numeros")
        sys.exit()

for tuplas in opciones:
    if tuplas[0] == "-h":
        print(ayuda)
        sys.exit()
    if tuplas[0] == "-s":
        suma = 0
        for elementos in args:
            suma = suma + int(elementos)
        print(suma)
    if tuplas[0] == "-r":
        print(int(args[0])-int(args[1]))
    
    if tuplas[0] == "-m":
        print(int(args[0])*int(args[1]))

    if tuplas[0] == "-d":
        print(int(args[0])/int(args[1]))
    
    if tuplas[0] == "-p":
        print(int(args[0])**int(args[1]))

            

#utilizacion del argparse
"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number",type=int)
args = parser.parse_args()
print(args.square**2)"""

"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v","--verbose", help="increase output verbosity",action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")"""

"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int, help="display a square of a given number")
parser.add_argument("-v", "--verbosity", type=int,choices=[0, 1, 2], help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity == 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity == 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
"""
"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,help="display the square of a given number")
parser.add_argument("-v", "--verbosity", action="count",default=0, help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity >= 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity >= 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)
"""