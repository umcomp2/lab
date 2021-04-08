#!/usr/bin/env python3
import os
import sys
import multiprocessing
import getopt

def f(rconn, wconn):
    data = rconn.recv()
    wconn.send(data.upper())

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
