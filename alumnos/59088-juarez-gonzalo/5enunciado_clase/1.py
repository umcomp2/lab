#!/usr/bin/env python3
import os
import sys
import mmap
import signal

import getopt

EOF = b""
PGSIZE = 4 << 10
MAPSIZE = PGSIZE
RWSIZE = 1024
shm = None

def getargs(argstr):
    opt, args = getopt.getopt(argstr, "f:", "file=")
    if len(opt) < 1 and len(opt[0]) < 2:
        raise ValueError("Faltan argumentos")

    fpath = opt[0][1]

    if not os.path.isfile(fpath):
        raise ValueError("El archivo %s no existe", fpath)
    return fpath

# ======================== CHILD ============================

SIGC = 0
def writing():
    global shm
    global SIGC
    SIGC |= 1
    shm.seek(0, os.SEEK_SET)
    data = shm.read()
    min2mayus = ord("A") - ord("a")
    c = b""

    shm.seek(0, os.SEEK_SET)
    for b in data:
        c =  b
        if ord("a") <= c and c <= ord("z"):
            c = b + min2mayus
        shm.write(c.to_bytes(1, byteorder="big"))

    shm.seek(0, os.SEEK_SET)
    sys.stdout.buffer.write(shm.read())
    os.kill(os.getppid(), signal.SIGUSR2)

def chld():
    global SIGC
    if not SIGC:
        writing()
    os._exit(os.EX_OK)

def csighandler(signum, frame):
    writing()

# ======================== PARENT ============================

def psighandler(signum, frame):
    global shm
    shm.seek(0, os.SEEK_SET)
    sys.stdout.write(shm.read().decode("utf8"))


if __name__ == "__main__":
    signal.signal(signal.SIGUSR1, csighandler)
    signal.signal(signal.SIGUSR2, psighandler)
    fpath = getargs(sys.argv[1:])
    rb = b""
    # map anon porque la consigna no habla de modificar el archivo original
    shm = mmap.mmap(-1, MAPSIZE)

    print("Escribiendo...")

    fd = os.open(fpath, os.O_RDONLY)
    while (rb := os.read(fd, RWSIZE)) != EOF:
        shm.write(rb)
    shm.write(EOF)
    os.close(fd)

    print("Hijo iniciado")
    pid = os.fork()
    if not pid:
        chld()

    os.kill(pid, signal.SIGUSR1)

    os.wait()
    shm.close()
    sys.exit(0)
