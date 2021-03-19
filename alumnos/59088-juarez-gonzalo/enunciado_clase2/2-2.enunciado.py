#!/usr/bin/env python3

import sys
import os
import mmap

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
        if not os.path.isfile(inp):
            raise IOError("invalid filename/s")

        fd_inp = os.open(inp, os.O_RDONLY)
        fd_out = os.open(out, os.O_WRONLY | os.O_CREAT)

        inp_mmap = mmap.mmap(fd_inp, 0, prot=mmap.PROT_READ)
        os.write(fd_out, inp_mmap)

        os.fchown(fd_out, os.getuid(), os.getgid())
        os.fchmod(fd_out, 0o644)

        os.close(fd_out)
        os.close(fd_inp)
    except Exception as err:
        sys.stdout.write(str(err))
        raise

if __name__ == "__main__":
    sys.stdout.write("archivo 1: ")
    sys.stdout.flush()
    arch1 = recv().decode("utf8")

    sys.stdout.write("archivo 2: ")
    sys.stdout.flush()
    arch2 = recv().decode("utf8")
    cp(arch1, arch2)
