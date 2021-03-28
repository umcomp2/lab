#!/usr/bin/env python3

import sys
import os
import mmap
import shutil

TERM = "\n\x00\r "
STDIN = 0
STDOUT = 1

# @fd           file descriptor de donde leer
# @nbytes       cantidad de bytes a leer
# @exclude      string de caracteres que se excluyen de los bytes leidos
def srecvn(fd=STDIN, nbytes=4096, exclude=TERM):
    ret = os.read(fd, nbytes).decode("utf8")
    for e in exclude:
        ret = ret.replace(e, "")
    return ret

# @src      path del archivo a ser copiado
# @dst      path del archivo destino
def copy(src, dst):
    try:
        src = os.path.realpath(src)
        if not os.path.isfile(src):
            raise IOError("%s no existe" % src)

        fd_src = os.open(src, os.O_RDONLY)
        src_mmap = mmap.mmap(fd_src, 0, prot=mmap.PROT_READ)

        with open(dst, "w") as dsthandle:
            dsthandle.write(src_mmap[:].decode())

        os.close(fd_src)
        shutil.copystat(src, dst)
    except Exception as err:
        sys.stdout.write(str(err))
        raise

if __name__ == "__main__":
    sys.stdout.write("src: ")
    sys.stdout.flush()
    src = srecvn()

    sys.stdout.write("dst: ")
    sys.stdout.flush()
    dst = srecvn()
    copy(src, dst)
