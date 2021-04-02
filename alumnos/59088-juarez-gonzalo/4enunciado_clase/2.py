#!/usr/bin/env python3
import os
import sys
import stat
import mmap
import signal
import struct

import getopt

RWSIZE = 256
STDIN_NO = 0
STDOUT_NO = 1

fpid = 0
spid = 0

def rot13(binput):
    out = bytearray()
    rango_alpha = ord("z") - ord("a")

    for i in range(len(binput)):
        a = binput[i]
        if ord("A") <= binput[i] and binput[i] <= ord("Z"):                   # está en el alfabeto y es mayúsucla
            a = (binput[i] - ord("A") + 13) % rango_alpha + ord("A")
        elif ord("a") <= binput[i] and binput[i] <= ord("z"):                 # está en el alfabeto y es minúscula
            a = (binput[i] - ord("a") + 13) % rango_alpha + ord("a")
        else:                                                                 # es simbolo desconocido, se deja como tal
            out += (binput[i]).to_bytes(1, byteorder="big")
            continue
        out += struct.pack("b", a)
    return out

def primer_hijo(fname):

    fd = os.open(fname, os.O_CREAT | os.O_TRUNC | os.O_RDWR, stat.S_IRUSR | stat.S_IWUSR)
    os.write(STDOUT_NO, b"\t(Apretar Ctrl-D para terminar la lectura\n)")

    while (rbytes := os.read(STDIN_NO, RWSIZE)) != b"":
        os.write(fd, rbytes)
    os.close(fd)

    os.kill(os.getppid(), signal.SIGUSR1)
    signal.sigwait([signal.SIGUSR1])

    fd = os.open(fname, os.O_RDONLY)
    while (rbytes := os.read(fd, RWSIZE)) != b"":
        os.write(STDOUT_NO, rbytes)
    os.kill(os.getppid(), signal.SIGUSR1)

    sys.exit(0)

def segundo_hijo(fname):
    signal.sigwait([signal.SIGUSR2])

    fd = os.open(fname, os.O_RDWR)
    fmmap = mmap.mmap(fd, 0)
    r13 = rot13(fmmap.read())
    fmmap.seek(0, os.SEEK_SET)
    fmmap.write(r13)

    fmmap.close()
    os.close(fd)

    os.kill(os.getppid(), signal.SIGUSR2)
    sys.exit(0)

def SIGUSR1_handler(signum, frame):
    os.kill(spid, signal.SIGUSR2)

def SIGUSR2_handler(signum, frame):
    os.kill(fpid, signal.SIGUSR1)

if __name__ == "__main__":
    try:
        opt, args = getopt.getopt(sys.argv[1:], "f:", "file=")
        if len(opt) < 1 or len(opt[0]) < 2:
            raise ValueError("faltan argumentos")
        fname = opt[0][1]
        signal.signal(signal.SIGUSR1, SIGUSR1_handler)
        signal.signal(signal.SIGUSR2, SIGUSR2_handler)

        fpid = os.fork()
        if not fpid:
            primer_hijo(fname)

        spid = os.fork()
        if not spid:
            segundo_hijo(fname)

        while os.wait():
            continue
    except ChildProcessError as err:
        if err.errno == 10:
            print("=============FIN ROT13=================")
            print("exit status de hijos recolectado")
