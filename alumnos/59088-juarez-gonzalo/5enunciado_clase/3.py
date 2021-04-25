#!/usr/bin/env python3
import os
import sys
import struct
import multiprocessing
import getopt

# @b_arr     bytearray con datos a pasar por rot13
def rot13(b_arr):
    r_alpha = ord("z") - ord("a") + 1
    out = bytearray()
    c = b""

    for b in b_arr:
        if ord("A") <= b and b <= ord("Z"):                 # está en el alfabeto, es mayúscula
            c = (b - ord("A") + 13) % r_alpha + ord("A")
            c = struct.pack("b", c)
        elif ord("a") <= b and b <= ord("z"):               # está en el alfabeto, es minúscula
            c = (b - ord("a") + 13) % r_alpha + ord("a")
            c = struct.pack("b", c)
        else:                                               # no está en el alfabeto, lo pasamos a bytes y dejamos como tal
            c = b.to_bytes(1, byteorder="big")
        out += c
    return out

def f(rconn, wconn):
    data = bytes(rconn.recv(), "utf8")
    wconn.send(rot13(data).decode("utf8"))

if __name__ == "__main__":
    opt, args = getopt.getopt(sys.argv[1:], "f:")
    if len(opt) < 1 or len(opt[0]) < 2:
        raise ValueError("faltan argumentos")
    fpath = opt[0][1]
    if not os.path.isfile(fpath):
        raise ValueError("argumento inválido")

    prc, cwc = multiprocessing.Pipe()
    crc, pwc = multiprocessing.Pipe()
    p = multiprocessing.Process(target=f, args=(crc, cwc))
    p.start()
    with open(fpath) as f:
        pwc.send(f.read())
        data = prc.recv()
    p.join()
    print(data)
