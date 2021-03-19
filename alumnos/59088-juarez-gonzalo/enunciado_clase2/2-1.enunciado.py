#!/usr/bin/env python3

import os
import sys

TERM = b"\n\x00\r "
STDIN = 0
STDOUT = 1

arch1 = ""
arch2 = ""

# @fd           file descriptor to read in
# @exclude      bytearray of characters that cut the reading
def recv(fd=STDIN, exclude=TERM):
    ret = bytearray()
    c = b''

    while (c := os.read(fd, 1)) and c not in exclude:
        ret += c

    return ret

# @inp      path to file to be copied
# @out      path to file to be copy of inp file
def cp(inp, out):
    try:

        inp = os.path.realpath(inp)
        out = os.path.realpath(out)
        c = b''

        if not os.path.isfile(inp):
            raise IOError("invalid filename/s")

        fd_inp = os.open(inp, os.O_RDONLY)
        fd_out = os.open(out, os.O_WRONLY | os.O_CREAT)

        while c := os.read(fd_inp, 1):
            os.write(fd_out, c)

        os.fchown(fd_out, os.getuid(), os.getgid())
        os.fchmod(fd_out, 0o644)

        os.close(fd_out)
        os.close(fd_inp)
    except Exception as err:
        sys.stdout.write(str(err))
        raise

def main():
    try:
        os.write(STDOUT, b"archivo 1: ")
        arch1 = recv().decode("utf8")

        os.write(STDOUT, b"archivo 2: ")
        arch2 = recv().decode("utf8")

        cp(arch1, arch2)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
