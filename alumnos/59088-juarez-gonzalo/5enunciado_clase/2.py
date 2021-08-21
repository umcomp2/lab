#!/usr/bin/env python3
import os
import sys
import struct
import getopt

RWSIZE = 4096
STDOUT_NO = 1

def usagendie():
    print("Usage: %s -f <path_to_file>" % __file__)
    sys.exit(1)

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

# @rfd  fd del extremo de lectura
# @wfd  fd del extremo de escritura
def r2rot13(rfd, wfd):
    while (rdata := os.read(rfd, RWSIZE)) != b"":
        os.write(wfd, rot13(rdata))


if __name__ == "__main__":
    try:
        # prefijos: c = child, p = parent
        cr = pw = pr = cw = -1
        opt, args = getopt.getopt(sys.argv[1:], "f:")
        if len(opt) < 1 or len(opt[0]) < 2:
            raise ValueError("faltan argumentos")
        fpath = opt[0][1]
        if not os.path.isfile(fpath):
            raise ValueError("argumento inválido")

        cr, pw = os.pipe()
        pr, cw = os.pipe()

        if not os.fork():
            os.close(pw)
            os.close(pr)
            r2rot13(cr, cw)
            os.close(cr)
            os.close(cw)
            os._exit(os.EX_OK)

        os.close(cr)
        os.close(cw)
        ffd = os.open(fpath, os.O_RDONLY)
        while (rbytes := os.read(ffd, RWSIZE)) != b"":
            os.write(pw, rbytes)
            uppercased = os.read(pr, RWSIZE)
            os.write(STDOUT_NO, uppercased)

    except ValueError as err:
        usagendie()
    finally:
        if pw != -1:
            os.close(pw)
        if pr != -1:
            os.close(pr)
