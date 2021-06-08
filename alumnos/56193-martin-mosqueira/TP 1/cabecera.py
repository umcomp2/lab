import argparse
import os
import re

def leer_cabecera(file):
    archivo=os.open(file, os.O_RDONLY)
    leer=os.read(archivo, 512)
    identificador=re.search(b'P[0-9]', leer)
    dimension=re.search(b'[^\n][0-9]{1,16}[^\n]\s[^\n][0-9]{1,16}', leer)
    profundidad=re.search(b'[\n][0-9]{1,16}[\n]', leer)

    if identificador:
        d=(dimension.group().decode("utf-8")).split()
        p=int(profundidad.group().decode("utf-8").replace('\n', ''))
        ancho=int(d[0])
        alto=int(d[1])
        off=int(profundidad.end())
        return(off,ancho,alto,p)
    else:
        print('error de formato')
