#!/usr/bin/env python3

# el objetivo de esto es spamear syscalls

import os
import sys

TERM = b"\n\x00\r "
STDIN = 0
STDOUT = 1

# @fd           file descriptor de donde leer
# @exclude      bytearray de caracteres que finalizan la lectura
def recv(fd=STDIN, exclude=TERM):
    ret = bytearray()
    c = b''

    while (c := os.read(fd, 1)) and c not in exclude:
        ret += c

    return ret

# @src      path del archivo a ser copiado
# @dst      path del archivo destino
def cp(src, dst):
    try:

        src = os.path.realpath(src)
        dst = os.path.realpath(dst)
        c = b''

        if not os.path.isfile(src):
            raise IOError("%s no existe" % src)

        fd_src = os.open(src, os.O_RDONLY)
        fd_dst = os.open(dst, os.O_WRONLY | os.O_CREAT)

        while c := os.read(fd_src, 1):
            os.write(fd_dst, c)

        os.fchown(fd_dst, os.getuid(), os.getgid())
        os.fchmod(fd_dst, 0o644)

        os.close(fd_dst)
        os.close(fd_src)
    except Exception as err:
        sys.stdout.write(str(err))
        raise

def main():
    try:
        os.write(STDOUT, b"src: ")
        src = recv().decode("utf8")

        os.write(STDOUT, b"dst: ")
        dst = recv().decode("utf8")

        cp(src, dst)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
