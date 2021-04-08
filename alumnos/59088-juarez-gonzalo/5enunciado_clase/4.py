#!/usr/bin/env python3
import os
import sys
import multiprocessing
import getopt

# ========= FORMATO MATRIZ EN EL ARCHIVO =========
#   siendo i un numero real en el sistema decimal
#   i11\ti12...\ti1n
#   i21\ti22...\ti2n
#   i31\ti32...\ti3n
#   ...
#   im1\tim2...\timn

BASE = 10

def parse_matriz(data):
    m = [[0]]
    col = 0
    row = 0
    prevflag = 0b00
    # prevflag: info sobre caracter previo
    # 0b00 -> era espacio en blanco
    # 0b01 -> era otro numero
    # 0b10 -> era signo negativo
    # 0b11 -> era otro numero de signo negativo
    num = 0
    for c in data:
        if c == "\n":
            col = 0
            row += 1
            prevflag &= 0b00
            continue
        if c == "\t":
            col += 1
            prevflag &= 0b00
            continue
        if c == "-":
            prevflag |= 0b10
            continue

        # el caracter previo correspondia a un numero y está guardado en num
        # acá num guarda el valor del numero previo
        if prevflag & 0b01:
            num = abs(num) * BASE
        else:
            num = 0

        # c no es uno de los caracteres especiales que consideramos
        # si c no es un numero, float levanta error
        num += float(c)

        # el caracter previo era un numero negativo y está en num
        # o simplemente era el signo negativo
        if prevflag & 0b10:
            num = -1 * num

        # la prox iteracion sabe que esta iteracion guardó un valor en num
        prevflag |= 0b01

        # la primera vez que se llega a una fila o columna, hay que agregarla
        # no es el caso para los numeros de varios digitos
        if len(m) < row+1:
            m.append([])
        if len(m[row]) < col+1:
            m[row].append(0)

        m[row][col] = num

    return m

def usagendie():
    print("Usage: %s [ --input | -i ] <filepath> [ -d | -m ] <num>" % __file__)
    sys.exit(1)

def div(a, b):
    return a / b

def mult(a, b):
    return a * b

def mult_row(row):
    global factor
    return [mult(a, factor) for a in row]

def div_row(row):
    global factor
    return [div(a, factor) for a in row]

if __name__ == "__main__":
    try:
        fc = None
        fpath = None
        factor = None
        outpath = None

        opt, args = getopt.getopt(sys.argv[1:], "d:m:i:o:", ["input=", "output="])
        if len(opt) < 2 or len(opt) > 3:
            raise ValueError("Numero de argumentos erróneo")

        for a in opt:
            if a[0] == "-d":
                fc = div_row
                factor = float(a[1])
            elif a[0] == "-m":
                fc = mult_row
                factor = float(a[1])
            elif a[0] == "--input" or a[0] == "-i":
                fpath = a[1]
            elif a[0] == "--output" or a[0] == "-o":
                outpath = a[1]
            else:
                raise ValueError("Argumento no reconocido")

        if fc == None or fpath == None:
            raise ValueError("Faltan argumentos")
        if not os.path.isfile(fpath):
            raise Exception("%d no existe o no es un archivo" % fpath)

        with open(fpath, "r") as f:
            data = f.read()
            m_in = parse_matriz(data)

        if outpath:
            sys.stdout = open(outpath, "w")

        with multiprocessing.Pool(len(m_in)) as p:
            m_out = p.map(fc, m_in)

        for row in m_out:
            sys.stdout.write(str(row) + "\n")

        if outpath:
            sys.stdout.close()

    except ValueError as err:
        usagendie()
