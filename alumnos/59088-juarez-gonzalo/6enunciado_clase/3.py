#!/usr/bin/env python3
import os
import sys
import stat

import multiprocessing as mp

import getopt

NCHILD = 3
EOF = b""

def pipe2file(q, fname, childnum):
    rb = b""
    newfname = "h%d-" % childnum
    newfname += fname
    fd = os.open(newfname, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, stat.S_IWUSR | stat.S_IRUSR)
    while (rb := q.get()) != EOF:
        os.write(fd, rb)

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

if __name__ == "__main__":
    fname = ""
    rwize = 0
    queues = []
    pool = []

    fname, rwsize = parseargs(sys.argv[1:])

    for i in range(NCHILD):
        queues.append(mp.Queue())

    for i in range(NCHILD):
        p = mp.Process(target=pipe2file, args=(queues[i], fname, i+1))
        pool.append(p)
        p.start()

    fd = os.open(fname, os.O_RDONLY)

    rb = b""
    while rb := os.read(fd, rwsize):
        for i in range(NCHILD):
            queues[i].put(rb)

    for i in range(NCHILD):
        queues[i].put(EOF) # manda EOF

    for i in range(NCHILD):
        pool[i].join()
