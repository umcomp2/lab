#!/usr/bin/env python3
import os
import sys
import getopt

RWSIZE = 4096
STDOUT_NO = 1

def usagendie():
    print("Usage: %s -f <path_to_file>" % __file__)
    sys.exit(1)

# @rfd  fd del extremo de lectura
# @wfd  fd del extremo de escritura
def r2upper2w(rfd, wfd):
    while (rdata := os.read(rfd, RWSIZE)) != b"":
        os.write(wfd, rdata.upper())


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
            r2upper2w(cr, cw)
            os._exit(os.EX_OK)

        ffd = os.open(fpath, os.O_RDONLY)
        while (rbytes := os.read(ffd, RWSIZE)) != b"":
            os.write(pw, rbytes)
            uppercased = os.read(pr, RWSIZE)
            os.write(STDOUT_NO, uppercased)

    except ValueError as err:
        usagendie()
    finally:
        if cr != -1:
            os.close(cr)
        if pw != -1:
            os.close(pw)
        if cw != -1:
            os.close(cw)
        if pr != -1:
            os.close(pr)
