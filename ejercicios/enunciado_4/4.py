#!/usr/bin/python3
import argparse
import os
import time

parser = argparse.ArgumentParser(description='python3 ej4.py -f pasar.txt')
parser.add_argument('-f', action="store", metavar='archivo', type=str,
                    required=True, help="Archivo a abrir")

args = parser.parse_args()

pph_r, pph_w = os.pipe()
php_r, php_w = os.pipe()
pid = os.fork()
#hijo
if pid == 0:
    print("Hijo iniciado\n")
    os.close(pph_w)
    os.close(php_r)
    while True:
        b_leido = os.read(pph_r, 1024)
        #leido = leido.replace("\n", "")
        leido = b_leido.decode('utf-8')
        if leido == '':
            break
        b_leido = leido.upper().encode('utf-8')
        os.write(php_w,b_leido)
    os.close(pph_r)
    os.close(php_w)
    exit()
#padre
else:
    os.close(pph_r)
    os.close(php_w)
    with open(args.f, 'r') as archi:
        print("\nEscribiendo...")
        for linea in archi:
            os.write(pph_w, linea.encode('utf-8'))
    archi.close()
    os.close(pph_w)
    while True:
        b_leido = os.read(php_r, 1024)
        #leido = leido.replace("\n", "")
        leido = b_leido.decode('utf-8')
        if leido == '':
            break
        os.write(1,b_leido)
    os.close(php_r)

os.wait()
