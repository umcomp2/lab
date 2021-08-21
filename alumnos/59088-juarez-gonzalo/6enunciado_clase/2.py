#!/usr/bin/env python3
import os
import sys
import stat

import multiprocessing as mp

import getopt

NCHILD = 3

def pipe2file(rpipe_end, fname, childnum):
    rb = b""
    newfname = "h%d-" % childnum
    newfname += fname
    fd = os.open(newfname, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, stat.S_IWUSR | stat.S_IRUSR)
    while rb := rpipe_end.recv():
        os.write(fd, rb)
    rpipe_end.close()

def parseargs(argv):
    opt, args = getopt.getopt(argv, "n:f:")
    fname = ""
    rwize = 0

    for o in opt:
        if o[0] == "-n":
            rwsize = int(o[1])
        elif o[0] == "-f":
            fname = o[1]

    if not fname or not rwsize:
        raise ValueError("Faltan parametros")

    return fname, rwsize

def init_pipes(nchild, rpipe_ends, wpipe_ends):
    for i in range(NCHILD):
        r, w = mp.Pipe(False)
        rpipe_ends.append(r)
        wpipe_ends.append(w)

def close_wpipes(nchild, wpipe_ends):
    for i in range(nchild):
        wpipe_ends[i].send(b"") # manda EOF
        wpipe_ends[i].close()

if __name__ == "__main__":
    fname = ""
    rwize = 0
    rpipe_ends = []
    wpipe_ends = []
    pool = []

    fname, rwsize = parseargs(sys.argv[1:])

    init_pipes(NCHILD, rpipe_ends, wpipe_ends)

    for i in range(NCHILD):
        p = mp.Process(target=pipe2file, args=(rpipe_ends[i], fname, i+1))
        pool.append(p)
        p.start()

    fd = os.open(fname, os.O_RDONLY)

    rb = b""
    while rb := os.read(fd, rwsize):
        for i in range(NCHILD):
            wpipe_ends[i].send(rb)

    close_wpipes(NCHILD, wpipe_ends)

    for i in range(NCHILD):
        pool[i].join()
