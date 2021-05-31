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
