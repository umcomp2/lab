import sys
import os
import stat

import mmap

from ppm_util import *
from header import *
INIT_RSIZE = 512            # tamaño de lectura inicial (usado para leer el header)

# =============== MAIN ================

if __name__ == "__main__":
    fname, rwsize = parse_args(sys.argv[1:])

    fd = os.open(fname, os.O_RDONLY)
    rb = os.read(fd, INIT_RSIZE)

    in_hdr = header_init()
    in_hdr["ops"]["parse"](in_hdr, rb)
    rwsize = PPM_ALIGN(rwsize, in_hdr["b_per_px"])

    out_hdr = header_cp(in_hdr)
    out_hdr["ops"]["swaprc"](out_hdr)

    in_fd = os.open(fname, os.O_RDONLY)
    hdrbytes = out_hdr["ops"]["calc_hdrbytes"](out_hdr)
    imgbytes = in_hdr["ops"]["calc_imgbytes"](in_hdr)
    totalbytes = hdrbytes + imgbytes

    out_shm = mmap.mmap(-1, totalbytes)
    out_shm.write(out_hdr["content"])

    os.lseek(in_fd, in_hdr["f_idx"], os.SEEK_SET)
    while rb := os.read(in_fd, imgbytes):
        bcount = len(rb)
        imgbytes -= bcount
        for b in range(bcount):
            in_pixel = (imgbytes + b) // 3
            offset = (imgbytes + b) % 3
            in_pos = hdrbytes + imgbytes + b

            in_r, in_c = in_hdr["ops"]["pixel2rc"](in_hdr, in_pixel)
            out_r = out_hdr["rows"] - in_c - 1
            out_c = in_r
            out_pixel = out_hdr["ops"]["rc2pixel"](out_hdr, out_r, out_c)
            out_pos = hdrbytes + 3 * out_pixel + offset

            out_shm[out_pos] = rb[b]

    totalbytes = in_hdr["ops"]["calc_totalbytes"](out_hdr)
    out_fd = os.open("rot.ppm", os.O_CREAT | os.O_RDONLY | os.O_WRONLY, stat.S_IRUSR | stat.S_IWUSR)
    wc = 0
    while wc < totalbytes:
        wb = os.write(out_fd, out_shm)
        wc += wb
