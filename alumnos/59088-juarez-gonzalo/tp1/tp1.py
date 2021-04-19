#!/usr/bin/env python3
import os
import stat
import sys
import getopt

import multiprocessing as mp
from multiprocessing.sharedctypes import Value
import mmap
import struct

RSIZE = 512
INFONL = 3  # total de lineas del header que aportan info en .ppm
EOF = b""
PPM_STEP = 3
HEADER = b""

# EL HEADER ES DE LA FORMA TIPO - COLSxROWS - MAX_BYTE_VAL
# LA CANTIDAD DE BYTES A LEER SE PUEDE OBTENER COMO LEN(HEADER) + COLSxROWS * 3 * (MAX_BYTE_VAL+1) >> 8

shm = None
empty_sem = None    # shm esta vacio
nonempty_sem = None # shm tiene contenido

read = 0         # indica la cantidad de readers que ya terminaron de leer shm
read_lock = None # lock sobre variable read
r_condvar = None # variable condicional que trabaja con read_lock

def PPM_ALIGN(size):
    global PPM_STEP
    return size // PPM_STEP * PPM_STEP  # siendo PPM_STEP no multiplo de 2, de lo contrario -> bitwise

def reader(rwsize, r_offset, fname):
    global HEADER
    global PPM_STEP
    global EOF
    global body_bytes

    global shm
    global empty_sem
    global nonempty_sem

    global r_condvar
    global r_lock
    global read

    b_count = 0 # cuenta la cantidad de bytes leidos de shm y escritos, si b_count == body_bytes entonces fin de la funcion

    out_fname = "h%d-" % (r_offset + 1)
    out_fname += fname

    out_fd = os.open(out_fname, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, stat.S_IWUSR | stat.S_IRUSR)
    os.write(out_fd, HEADER)

    nonempty_sem.acquire()
    while True:

        shm.seek(0, os.SEEK_SET)
        rb = shm.read(rwsize)
        wb = bytearray()

        for i in range(0, rwsize, PPM_STEP):
            int_byte = rb[i + r_offset]
            wb += int_byte.to_bytes(1, byteorder="big")

        #prnt = bytes("============= READER %d ============" % (r_offset + 1), "utf8")
        #prnt += wb
        #sys.stdout.buffer.write(prnt)
        #sys.stdout.flush()
        os.write(out_fd, wb)

        r_lock.acquire()
        read.value += 1
        #print("read value incrementing %d" % read.value)
        #sys.stdout.flush()
        if read.value != PPM_STEP:
            #print("waiting for rest to read")
            #sys.stdout.flush()
            r_condvar.wait()
        else:
            r_condvar.notify_all()
            empty_sem.release()
        read.value -= 1
        #print("read value decrementing %d" % read.value)
        #sys.stdout.flush()
        r_lock.release()

        nonempty_sem.acquire()
    sys.stdout.buffer.write(bytes("============== END OF READER %d ===============" % r_offset, "utf8"))
    sys.stdout.flush()
    nonempty_sem.release()

def writer(fd, s_idx, rwsize):
    global EOF

    global shm
    global empty_sem
    global nonempty_sem

    rb = b""

    os.lseek(fd, s_idx, os.SEEK_SET)
    while (rb := os.read(fd, rwsize)) != EOF:
        empty_sem.acquire()

        #prnt = bytearray()
        #prnt += b"============ WRITER ============="
        #prnt += rb
        #sys.stdout.buffer.write(prnt)
        #sys.stdout.flush()
        shm.seek(0, os.SEEK_SET)
        shm.write(rb)

        nonempty_sem.release()
        nonempty_sem.release()
        nonempty_sem.release()

    sys.stdout.buffer.write(b"============== END OF WRITER ===============")
    sys.stdout.flush()
    empty_sem.acquire()
    shm.seek(0, os.SEEK_SET)
    shm.write(EOF)
    nonempty_sem.release()
    nonempty_sem.release()
    nonempty_sem.release()

def parse_args(argv):
    opt, args = getopt.getopt(argv, "n:f:")
    fname = ""
    rwsize = 0

    for o in opt:
        if o[0] == "-n":
            rwsize = int(o[1])
        elif o[0] == "-f":
            fname = o[1]

    if not fname or not rwsize:
        raise ValueError("Faltan parametros")

    # super mega validacion de formato de archivo
    if ".ppm" != fname[-4:]:
        raise ValueError("Archivo no tiene extensión ppm")

    return fname, rwsize

def parse_header(rb):
    global INFONL
    nls = 0     # contador de '\n' en lineas que aportan info
    f_idx = 0   # indice posterior al ultimo newline de linea que aporta info
    cmmnt = 0   # flag que indica si prox '\n' corresponde a linea de comentario
    c = b""

    for i in range(len(rb)):
        if rb[i] == ord('#'):
            cmmnt |= 1
            continue
        if rb[i] == ord('\n') and cmmnt:
            cmmnt &= 0
            continue
        if rb[i] == ord('\n'):
            nls += 1
        if nls == INFONL:
            f_idx = i + 1
            break

    if nls != INFONL:
        raise ValueError("Demasiados comentarios en el header, header superior a %d bytes" % RSIZE)

    return f_idx

if __name__ == "__main__":
    fname, rwsize = parse_args(sys.argv[1:])

    fd = os.open(fname, os.O_RDONLY)

    shm = mmap.mmap(-1, rwsize)
    empty_sem = mp.Semaphore(1)
    nonempty_sem = mp.Semaphore(0)

    r_lock = mp.Lock()
    r_condvar = mp.Condition(r_lock)
    read = mp.sharedctypes.Value('i', 0, lock=False)

    os.lseek(fd, 0, os.SEEK_SET)
    rb = os.read(fd, RSIZE)

    f_idx = parse_header(rb)
    HEADER = rb[:f_idx]

    rwsize = PPM_ALIGN(rwsize)

    for i in range(PPM_STEP):
        p = mp.Process(target=reader, args=(rwsize, i, fname))
        p.start()

    writer(fd, f_idx, rwsize)

    os.close(fd)
