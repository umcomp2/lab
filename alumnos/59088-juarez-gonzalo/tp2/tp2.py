import os
import stat

import sys

from ppm_util import *
from header import *

INIT_RSIZE = 512            # tamaño de lectura inicial (usado para leer el header)

# =============== MAIN ================

if __name__ == "__main__":
    fname, rwsize = parse_args(sys.argv[1:])

    fd = os.open(fname, os.O_RDONLY)
    rb = os.read(fd, INIT_RSIZE)

    hdr = header_init()
    hdr["ops"]["parse"](hdr, rb)
    rwsize = PPM_ALIGN(rwsize, hdr["b_per_px"])

    out_hdr = header_cp(hdr)
    out_hdr["ops"]["swaprc"](out_hdr)

    out_fd = os.open("rot%s" % fname, os.O_RDONLY | os.O_WRONLY | os.O_CREAT, stat.S_IRUSR | stat.S_IWUSR)
    fd = os.open(fname, os.O_RDONLY)

    os.write(out_fd, out_hdr["content"])
    r_acc = 0
    while (rb := os.read(fd, totalbytes - racc)) != EOF:
        os.write(out_fd, rb)
        r_acc += len(rb)
