import sys
import os
import mmap
import stat
import threading

from parse import *
from rot import *

NCHILD = NCOLORS

out_mmap = None
rc_rot = None


# =============== shm & shm sync ================
#
#   Sincronizacion necesaria en algoritmo producer-consumer

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
            out_byte = byte_rot(rc_rot, in_header, out_header, rbc + color_byte)
            out_mmap[out_byte] = rb[color_byte]
        rbc += n

        c_barrier.wait()

def producer(in_header, filepath, rsize, nconsum):
    rb = b""
    in_fd = os.open(filepath, os.O_RDONLY)

    os.lseek(in_fd, HEADERSIZE(in_header), os.SEEK_SET)
    while (rb := os.read(in_fd, rsize)) != b"":
        empty_sem.acquire()

        shm.seek(0, os.SEEK_SET)
        shm.write(rb)

        for i in range(nconsum):
            nonempty_sem.release()

def w_mmap2file(out_filename):
    out_fd = os.open(out_filename, os.O_CREAT | os.O_RDONLY | os.O_WRONLY, stat.S_IRUSR | stat.S_IWUSR)
    wc = 0
    totalsize = FILESIZE(out_header)
    while wc < totalsize:
        wb = os.write(out_fd, out_mmap[wc:])
        wc += wb
    os.close(out_fd)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    if args["rotopt"] == WALSH:
        rc_rot = walsh_rc_rot
    elif args["rotopt"] == CW:
        rc_rot = cw_rc_rot
    else:
        rc_rot = ccw_rc_rot

    colorfilter = args["colorfilter"]
    doswap = args["rotopt"] != WALSH

    in_header = search_fileheader(args["filepath"])
    out_header = header_cp(in_header)

    if doswap:
        swap_rc(out_header)

    nconsum = 0
    for i in range(NCHILD):
        if 1 << i & colorfilter:
            nconsum += 1

    out_mmap = mmap.mmap(-1, FILESIZE(out_header))
    out_mmap.write(out_header["content"])

    rsize = PPM_ALIGN(in_header, args["rsize"])

    shm = mmap.mmap(-1, rsize)
    empty_sem = threading.Semaphore(1)
    nonempty_sem = threading.Semaphore(0)

    c_barrier = threading.Barrier(nconsum, empty_sem_up)

    pool = []
    for i in range(NCHILD):
        if 1 << i & colorfilter:
            pool.append(threading.Thread(target=consumer, args=(in_header, out_header, rsize, i)))
            pool[-1].start()

    producer(in_header, args["filepath"], rsize, nconsum)
    for p in pool:
        p.join()

    if args["rotopt"] == WALSH:
        out_filename = "walsh." + args["filename"]
    elif args["rotopt"] == CW:
        out_filename = "cw." + args["filename"]
    else:
        out_filename = "ccw." + args["filename"]

    w_mmap2file(out_filename)

    shm.close()
    out_mmap.close()
