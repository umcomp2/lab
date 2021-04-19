#!/usr/bin/env python3
import os
import stat
import sys
import getopt

import multiprocessing as mp
from multiprocessing.sharedctypes import Value
import mmap

# ================ Ayuda general a lo largo del programa ================

RSIZE = 512
INFONL = 3  # total de lineas del header que aportan info en .ppm
EOF = b""
PPM_STEP = 3
FILLER_B = b"\x00\x00\x00"

def PPM_ALIGN(size):
    global PPM_STEP
    return size // PPM_STEP * PPM_STEP  # siendo PPM_STEP no multiplo de 2, de lo contrario -> bitwise

def btoi(b_arr):
    ret = 0
    for i in range(len(b_arr)):
        ret = ret * 10 + (b_arr[i] - ord('0'))
    return ret

# =============== Diccionario para el header y funciones correspondientes ================

# EL HEADER ES DE LA FORMA TIPO - COLSxROWS - MAX_BYTE_VAL
# LA CANTIDAD DE BYTES A LEER SE PUEDE OBTENER COMO LEN(HEADER) + COLSxROWS * 3 * (MAX_BYTE_VAL+1) >> 8

def h_calc_colorsize(header):
    return (header["maxcolor"] + 1) >> 8

def h_calc_totalbytes(header):
    global PPM_STEP
    return h_calc_colorsize(header) * PPM_STEP * header["cols"] * header["rows"]

HEADER = {
    "content": "",
    "f_idx": "",
    "magic": "",
    "cols": 0,
    "rows": 0,
    "maxcolor": 0,
    "calc_totalbytes": h_calc_totalbytes,
    "calc_colorsize": h_calc_colorsize,
}

# =============== Sincronizacion sobre la memoria compartida ================

shm = None
empty_sem = None    # shm esta vacio
nonempty_sem = None # shm tiene contenido

# =============== Sincronizacion sobre readers ===============
#   Un reader que haya terminado con el bloque A,
#   no puede empezar a leer un bloque B sin esperar a que el resto
#   de los readers haya terminado de leer el bloque A

read = 0         # indica la cantidad de readers que ya terminaron de leer shm
read_lock = None # lock sobre variable read
r_condvar = None # variable condicional que trabaja con read_lock


def reader(rwsize, r_offset, fname):
    global HEADER
    global PPM_STEP
    global FILLER_B

    global shm
    global empty_sem
    global nonempty_sem

    global r_condvar
    global r_lock
    global read

    b_count = 0 # cuenta la cantidad de bytes leidos de shm
    leftbytes = HEADER["calc_totalbytes"](HEADER)  # la cantidad total de bytes en .ppm sin header

    out_fname = "h%d-" % (r_offset + 1)
    out_fname += fname

    out_fd = os.open(out_fname, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, stat.S_IWUSR | stat.S_IRUSR)
    os.write(out_fd, HEADER["content"])

    nonempty_sem.acquire()
    while True:

        shm.seek(0, os.SEEK_SET)
        rsize = rwsize if rwsize < leftbytes else leftbytes
        rb = shm.read(rsize)

        b_count += len(rb)

        wb = bytearray()

        for i in range(0, rsize, PPM_STEP):
            int_byte = rb[i + r_offset]
            int_byte = int_byte.to_bytes(1, byteorder="big")
            wb += FILLER_B[:r_offset] + int_byte + FILLER_B[r_offset + 1:]

        os.write(out_fd, wb)
        leftbytes -= len(wb)

        # creo que en este bloque de sincronizacion entre readers hay un problema
        r_lock.acquire()
        read.value += 1
        if read.value != PPM_STEP:
            r_condvar.wait()
        else:
            empty_sem.release()
            r_condvar.notify_all()
        read.value -= 1
        r_lock.release()

        if not leftbytes:
            break

        nonempty_sem.acquire()

    sys.stdout.buffer.write(bytes("============== END OF READER %d, read: %d, left: %d ===============\n" % (r_offset, b_count, leftbytes), "utf8"))
    sys.stdout.flush()
    nonempty_sem.release()

def writer(fd, s_idx, rwsize):
    global EOF
    global PPM_STEP

    global shm
    global empty_sem
    global nonempty_sem

    rb = b""
    b_count = 0

    os.lseek(fd, s_idx, os.SEEK_SET)
    while (rb := os.read(fd, rwsize)) != EOF:
        b_count += len(rb)
        empty_sem.acquire()

        shm.seek(0, os.SEEK_SET)
        shm.write(rb)

        for i in range(PPM_STEP):
            nonempty_sem.release()

    sys.stdout.buffer.write(bytes("============== END OF WRITER, written: %d ===============\n" % b_count, "utf8"))
    sys.stdout.buffer.flush()

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
    global HEADER

    hdr_no_cmmnt = bytearray()
    nls = 0         # contador de '\n' en lineas que aportan info
    nls_idx = []
    f_idx = 0       # indice posterior al ultimo newline de linea que aporta info
    in_cmmnt = 0    # flag que indica si prox '\n' corresponde a linea de comentario
    c = b""

    for i in range(len(rb)):

        if rb[i] == ord('#'):
            in_cmmnt |= 1
        elif rb[i] == ord('\n') and in_cmmnt:
            in_cmmnt &= 0
            continue
        elif rb[i] == ord('\n'):
            nls_idx.append(i)
            nls += 1

        if not in_cmmnt:
            hdr_no_cmmnt += rb[i].to_bytes(1, byteorder="big")

        if nls == INFONL:
            f_idx = i + 1
            break

    if nls != INFONL:
        raise ValueError("Demasiados comentarios en el header, header superior a %d bytes" % RSIZE)

    hdr_fields = hdr_no_cmmnt.split(b'\n')

    HEADER["content"] = rb[:f_idx]
    HEADER["f_idx"] = f_idx

    HEADER["magic"] = hdr_fields[0].decode()

    HEADER["cols"], HEADER["rows"] = hdr_fields[1].split(b" ")
    HEADER["cols"] = btoi(HEADER["cols"])
    HEADER["rows"] = btoi(HEADER["rows"])

    HEADER["maxcolor"] = btoi(hdr_fields[2])

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

    parse_header(rb)

    rwsize = PPM_ALIGN(rwsize)

    for i in range(PPM_STEP):
        p = mp.Process(target=reader, args=(rwsize, i, fname))
        p.start()

    writer(fd, HEADER["f_idx"], rwsize)

    os.close(fd)
