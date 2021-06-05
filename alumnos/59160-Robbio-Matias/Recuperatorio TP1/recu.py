#!/usr/bin/python3
import argparse
import os


def multiplo3(num):
    aprox=num-(num%3)
    return aprox

def header_size(fd):
    lectura = os.read(fd, 50)
    lectura = lectura.split(b'\n')
    size = 0
    for i in range(0,len(lectura)):
        if lectura[i] == b'255':
            break
        size += (len(lectura[i])+1)
    size += (len(lectura[i])+1)
    return size 

def generador_filtro_R(fd,multiplicador):
    fd_new= 'r_' + fd
    os.open(fd_new)
    
def padre(fd,size):
    pass


    

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tp1 - procesa ppm')
    parser.add_argument('-s', '--size',action="store", type= int, required=True, help="Bloque de lectura(Preferentemente un numero multiplo de 3)")
    parser.add_argument('-r', '--red_multiplier',action="store", type=float,default=1, required=False, help="Intensidad del color en el filtro rojo")
    parser.add_argument('-g', '--green_multiplier',action="store", type=float,default=1, required=False, help="Intensidad del color en el filtro verde")
    parser.add_argument('-b', '--blue_multiplier',action="store", type=float,default=1, required=False, help="Intensidad del color en el filtro azul")
    parser.add_argument('-f', '--file',action="store", required=True, type=str, help="Imagen que se usara")
    args =  parser.parse_args()

    x=multiplo3(args.size)
    print(f"Se leeran bloques de {x} bytes")
   
    print(generador_filtro_R(args.file,args.red_multiplier))
