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
MMAPSIZE = 1 << 12 # 1MB en hackerman

FFLAG = 0
FFLAGSIZE = 8
SFLAG = 0
SFLAGSIZE = 8

fpid = 0
spid = 0

def usagendie():
    print("Usage: %s [ -f | --file ] <output_file>" % __file__)
    sys.exit(1)

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

def primer_hijo(fname, anonmap):
    global FFLAG
    global SFLAG
    print("primer hijo")
    rb = 0
    rbacc = 0
    fd = -1

    os.write(STDOUT_NO, b"\t(Apretar Ctrl-D para terminar la lectura\n)")
    while (rbytes := os.read(STDIN_NO, RWSIZE)) != b"":
        anonmap.write(rbytes)

    FFLAG[0] |= 1
    os.kill(os.getppid(), signal.SIGUSR1)

    while not SFLAG[0]:                     # spid aún no escribe a anonmap
        print("1 waiting")
        signal.sigwait([signal.SIGUSR2])
    SFLAG[0] &= 0
    print("continua primer hijo")

    anonmap.seek(0, os.SEEK_SET)
    fd = os.open(fname, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, stat.S_IWUSR)
    while (rb := os.write(fd, anonmap[rbacc:])):
        rbacc += rb

    anonmap.seek(0, os.SEEK_SET)
    print("=======INICIO ROT13========")
    print(anonmap.read().decode("utf8"))
    print("=========FIN ROT13=========")

    os._exit(os.EX_OK)

def segundo_hijo(anonmap):
    global FFLAG
    global SFLAG
    r13 = b""

    while not FFLAG[0]:                     # fpid aún no escribe a anonmap
        signal.sigwait([signal.SIGUSR2])
    FFLAG[0] &= 0

    anonmap.seek(0, os.SEEK_SET)
    r13 = rot13(anonmap.read())
    anonmap.seek(0, os.SEEK_SET)
    anonmap.write(r13)
    print("presig 2do hijo")

    SFLAG[0] |= 1
    os.kill(os.getppid(), signal.SIGUSR2)
    print("exit 2")
    os._exit(os.EX_OK)

def SIGUSR1_handler(signum, frame):
    global FFLAG
    global spid
    while FFLAG[0]:
        if spid != -1:
            os.kill(spid, signal.SIGUSR2)

def SIGUSR2_handler(signum, frame):
    global SFLAG
    global fpid
    print(os.getpid() != fpid)
    while SFLAG[0]:
        if fpid != -1:
            os.kill(fpid, signal.SIGUSR2)

if __name__ == "__main__":
    try:
        opt, args = getopt.getopt(sys.argv[1:], "f:", "file=")
        if len(opt) < 1 or len(opt[0]) < 2:
            raise ValueError("faltan argumentos")
        fname = opt[0][1]

        anonmap = mmap.mmap(-1, MMAPSIZE)

        FFLAG = mmap.mmap(-1, FFLAGSIZE)
        FFLAG[0] = 0    # fpid no ha escrito a anonmap
        SFLAG = mmap.mmap(-1, SFLAGSIZE)
        SFLAG[0] = 0    # spid no ha escrito a anonmap

        fpid = os.fork()
        if not fpid:
            primer_hijo(fname, anonmap) # no retorna
        spid = os.fork()
        if not spid:
            segundo_hijo(anonmap)       # no retorna

        signal.signal(signal.SIGUSR1, SIGUSR1_handler)
        signal.signal(signal.SIGUSR2, SIGUSR2_handler)

        while os.wait():
            continue
    except ChildProcessError as err:
        if err.errno == 10:
            print("exit status de hijos recolectado")
            sys.exit(0)
    except ValueError:
        usagendie()
