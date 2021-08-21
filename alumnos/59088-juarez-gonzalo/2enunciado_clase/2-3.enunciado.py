#!/usr/bin/env python3
import sys
import os

# @src      path del archivo a ser copiado
# @dst      path del archivo destino
def cp(src, dst):
    try:
        src = os.path.realpath(src)
        if not os.path.isfile(src):
            raise IOError("%s no existe" % src)

        with open(src, "r") as srchandle, open(dst, "w") as dsthandle:
            for line in srchandle:
                dsthandle.write(line)
    except Exception as err:
        print(str(err))
        raise

if __name__ == "__main__":
    src = str(input("src: "))
    dst = str(input("dst: "))
    cp(src, dst)
