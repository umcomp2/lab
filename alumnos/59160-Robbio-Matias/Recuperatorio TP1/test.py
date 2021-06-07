#!/usr/bin/python3
import argparse
import os
from multiprocessing import Pipe,Process


def multiplo3(num):
    aprox=int(num-(num%3))
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
    os.lseek(fd,0,0)
    return size 

def escalar_valor(byte,escala):
    value = int.from_bytes(byte,'big')
    value = round(value*escala)
    if value > 255:
        value = 255
    return value.to_bytes(1,'big')

def generador_filtro(color,nombre_archivo,escala,header,chunk,size):
    archivo_new= str(f'{color}_') + str(nombre_archivo)
    filtro = os.open(archivo_new,os.O_RDWR | os.O_CREAT)
    os.write(filtro,header)
    while True:
        pixels=list()
        for i in chunk:
            pixels.append(bytes([i]))
        if color == 'r':
            for i in range(0,len(pixels)-1,3):
                pixels[i] = escalar_valor(pixels[i],escala)
                pixels[i+1] = b'\x00'
                pixels[i+2] = b'\x00'
        elif color == 'g':
            for i in range(1,len(pixels),3):
                pixels[i-1] = b'\x00'
                pixels[i] = escalar_valor(pixels[i],escala)
                pixels[i+1] = b'\x00'
        elif color == 'b':
            for i in range(2,len(pixels),3):
                pixels[i-2] = b'\x00'
                pixels[i-1] = b'\x00'
                pixels[i] = escalar_valor(pixels[i],escala)
        pixels_mod = b''
        for i in pixels:
            pixels_mod = pixels_mod + i
        if len(chunk) < size:
            break
    os.lseek(filtro,header_size(filtro),0)
    os.write(filtro,pixels_mod)
            
            
         
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tp1 - procesa ppm')
    parser.add_argument('-s', '--size',action="store", type= int, required=True, help="Bloque de lectura(Preferentemente un numero multiplo de 3)")
    parser.add_argument('-r', '--red_multiplier',action="store", type=float,default=1, required=False, help="Intensidad del color en el filtro rojo")
    parser.add_argument('-g', '--green_multiplier',action="store", type=float,default=1, required=False, help="Intensidad del color en el filtro verde")
    parser.add_argument('-b', '--blue_multiplier',action="store", type=float,default=1, required=False, help="Intensidad del color en el filtro azul")
    parser.add_argument('-f', '--file',action="store", required=True, type=str, help="Imagen que se usara")
    args =  parser.parse_args()

    foto = os.open(args.file,os.O_RDONLY)
    os.lseek(foto,0,0)
    print(header_size(foto))
    header = os.read(foto,header_size(foto))
    size = args.size
    os.lseek(foto,header_size(foto),0)
    chunk = os.read(foto,size)
    generador_filtro('r',args.file,1,header,chunk,size)
    generador_filtro('g',args.file,1,header,chunk,size)
    print(generador_filtro('b',args.file,1,header,chunk,size))
    print(header)
    