import os
import mmap
import argparse


memoria = mmap.mmap(-1,100) #Creo la mem compartida
parser = argparse.ArgumentParser(description="python3 ej1.py -f pasar.txt")
parser.add_argument("-f", action="store", metavar="archivo", type=str, required=True, help="Archivo a abrir")

args = parser.parse_args()

pid = os.fork()

#Hijo
if pid == 0:
    leido = memoria.read()
    print(leido)
    b_leido = leido.upper()
else:
    with open(args.f, 'r') as archi:
        print("\nEscribiendo...")
        with mmap.mmap(f.fileno(), 0, acces=mmap.ACCES_READ) as m:
            print(m.read(1024)



