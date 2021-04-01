#!/usr/bin/env python3
import os
import sys
import getopt

RFIFO = "rfifo5a"
WFIFO = "wfifo5a"
RWSIZE = 256
STDOUT_NO = 1

def usagendie():
    print("Usage: %s -f <path_to_file>" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    try:
        ffd = rfd = wfd = -1
        opt, args = getopt.getopt(sys.argv[1:], "f:")
        if len(opt) < 1 or len(opt[0]) < 2:
            raise ValueError("faltan argumentos")
        fpath = opt[0][1]
        if not os.path.isfile(fpath):
            raise ValueError("argumento inválido")

        if not os.path.exists(RFIFO):
            os.mkfifo(RFIFO, 0o664)
        if not os.path.exists(WFIFO):
            os.mkfifo(WFIFO, 0o664)

        ffd = os.open(fpath, os.O_RDONLY)
        # primero RFIFO después WFIFO
        # el programa del otro lado del FIFO
        # debe abrir primero RFIFO y después WFIFO
        # si lo hace al reves -> deadlock (man 3 mkfifo)
        rfd = os.open(RFIFO, os.O_RDONLY)
        wfd = os.open(WFIFO, os.O_WRONLY)

        while (rbytes := os.read(ffd, RWSIZE)) != b"":
            os.write(wfd, rbytes)
            uppercased = os.read(rfd, RWSIZE)
            os.write(STDOUT_NO, uppercased)

    except ValueError as err:
        usagendie()
    finally:
        if rfd != -1:
            os.close(rfd)
            os.unlink(RFIFO)
        if wfd != -1:
            os.close(wfd)
            os.unlink(WFIFO)
        if ffd != -1:
            os.close(ffd)
