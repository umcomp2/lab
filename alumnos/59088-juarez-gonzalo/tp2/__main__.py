import sys
import os
import mmap
import stat
import threading

from headerutils import *
from parse import *

NCHILD = NCOLORS
NCONSUM = NCOLORS

out_mmap = None

rc_rot = None

def r_rc_rot(out_header, in_r, in_c):
    out_r = out_header["rows"] - in_c - 1
    out_c = in_r
    return out_r, out_c

def l_rc_rot(out_header, in_r, in_c):
    out_r = in_c
    out_c = out_header["cols"] - in_r - 1
    return out_r, out_c

def byte_rot(in_header, out_header, in_offset):
    in_pixel = BODYPX_OFFSET(in_header, in_offset)

    in_r, in_c = PIXEL2RC(in_header, in_pixel)
    out_r, out_c = rc_rot(out_header, in_r, in_c)

    out_pixel = RC2PIXEL(out_header, out_r, out_c)
    out_pos = HEADERSIZE(out_header) + BODYBYTE_OFFSET(out_header, out_pixel, in_offset)
    return out_pos

# =============== shm & shm sync ================
#
#   Sincronizacion necesaria en algoritmo producer-consumer estandar

shm = None          # el buffer compartido
empty_sem = None    # shm esta vacio
nonempty_sem = None # shm tiene contenido

# =============== consumers sync ===============
#
#   Sincronizacion necesaria para que todos los consumers
#   lean bloque a bloque a la par

c_barrier = None

def empty_sem_up():
    empty_sem.release()

def consumer(in_header, out_header, rsize, color_offset):
    leftbytes = BODYSIZE(out_header)
    rbc = 0
    b_per_px = BYTES_PER_PX(out_header)

    while leftbytes:
        nonempty_sem.acquire()

        n = rsize if rsize < leftbytes else leftbytes
        shm.seek(0, os.SEEK_SET)
        rb = shm.read(n)
        leftbytes -= n
        for b in range(0, n, b_per_px):
            color_byte = b + color_offset
            out_pos = byte_rot(in_header, out_header, rbc + color_byte)
            out_mmap[out_pos] = rb[color_byte]
        rbc += n

        c_barrier.wait()

def producer(in_header, filepath, rsize):
    rb = b""
    in_fd = os.open(filepath, os.O_RDONLY)

    os.lseek(in_fd, HEADERSIZE(in_header), os.SEEK_SET)
    while (rb := os.read(in_fd, rsize)) != b"":
        empty_sem.acquire()

        shm.seek(0, os.SEEK_SET)
        shm.write(rb)

        for i in range(NCONSUM):
            nonempty_sem.release()

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    if args["sentido"]:
        rc_rot = r_rc_rot
    else:
        rc_rot = l_rc_rot

    in_header = search_fileheader(args["filepath"])
    out_header = header_cp(in_header)
    swap_rc(out_header)

    out_mmap = mmap.mmap(-1, FILESIZE(out_header))
    out_mmap.write(out_header["content"])

    rsize = PPM_ALIGN(in_header, args["rsize"])

    shm = mmap.mmap(-1, rsize)
    empty_sem = threading.Semaphore(1)
    nonempty_sem = threading.Semaphore(0)

    c_barrier = threading.Barrier(NCHILD, empty_sem_up)

    pool = []
    for i in range(NCHILD):
        pool.append(threading.Thread(target=consumer, args=(in_header, out_header, rsize, i)))
        pool[i].start()

    producer(in_header, args["filepath"], rsize)
    for p in pool:
        p.join()

    #in_fd = os.open(args["filename"], os.O_RDONLY)
    #os.lseek(in_fd, HEADERSIZE(in_header), os.SEEK_SET)

    #left = BODYSIZE(in_header)
    #bcount = 0
    #while rb := os.read(in_fd, left):
    #    bcount = len(rb)
    #    left -= bcount
    #    for b in range(bcount):
    #        out_pos = byte_rot(in_header, out_header, left + b)
    #        out_mmap[out_pos] = rb[b]

    out_fd = os.open("rot.ppm", os.O_CREAT | os.O_RDONLY | os.O_WRONLY, stat.S_IRUSR | stat.S_IWUSR)
    wc = 0
    totalsize = FILESIZE(out_header)
    while wc < totalsize:
        wb = os.write(out_fd, out_mmap[wc:])
        wc += wb
    os.close(out_fd)
    shm.close()
    out_mmap.close()
