#!/usr/bin/env python3
import os
import stat
import sys
import getopt

import multiprocessing as mp
from multiprocessing.sharedctypes import Value
import mmap

# TODO:
#   -   Armar el histograma
#       Con un hashmap con tantas entradas como HEADER["maxcolor"], inicializadas a 0
#       y aumentando el contador a medida que se encuentra el numero de la entrada correspondiente
#       creo que se puede hacer rapido y facil. Quizás no estéticamente pero meeeeeeeh

# ================ Ayuda general a lo largo del programa ================

EOF = b""
RSIZE = 512
INFONL = 3  # total de lineas del header que aportan info en .ppm
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
# EL HEADER SIN COMENTARIOS ES DE LA FORMA: MAGIC\nCOLS ROWS\nMAX_BYTE_VAL\n
# LA CANTIDAD DE BYTES A LEER SE PUEDE OBTENER COMO LEN(HEADER) + COLS * ROWS * 3 * (MAX_BYTE_VAL+1) >> 8
# LA CANTIDAD DE BYTES SIN EL HEADER (calculada en h_calc_totalbytes) COMO COLS * ROWS * 3 * (MAX_BYTE_VAL+1) >> 8

def h_calc_colorsize(header):
    return (header["maxcolor"] + 1) >> 8

def h_calc_totalbytes(header):
    global PPM_STEP
    return header["hdr_ops"]["calc_colorsize"](header) * PPM_STEP * header["cols"] * header["rows"]

HDR_OPS = {
    "calc_totalbytes": h_calc_totalbytes,
    "calc_colorsize": h_calc_colorsize,
}

HEADER = {
    "content": "",
    "f_idx": "",
    "magic": "",
    "cols": 0,
    "rows": 0,
    "maxcolor": 0,
    "hdr_ops": HDR_OPS
}

# =============== Sincronizacion sobre la memoria compartida ================

shm = None
empty_sem = None    # shm esta vacio
nonempty_sem = None # shm tiene contenido

# =============== Sincronizacion sobre readers ===============
#   Un reader que haya terminado con el bloque A,
#   no puede empezar a leer un bloque B sin esperar a que el resto
#   de los readers haya terminado de leer el bloque A

rcount = 0         # indica la cantidad de readers que ya terminaron de leer shm
read_lock = None   # lock sobre variable rcount
r_condvar = None   # variable condicional que trabaja con read_lock

# =============== Algoritmo  ================
# Producer-Consumer modificado para sincronizar lectura de bloques entre consumers

def write_hist(col_count, fname):
    hist = bytearray()      # si esto fuera a parar al stack entonces es media nefasta la cuestion. pero es python
    hist_fname = fname + ".hist"
    hist_fd = os.open(hist_fname, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, stat.S_IWUSR | stat.S_IRUSR)

    for key in col_count.keys():
        hist += bytes("%d:\t%d\n" % (key, col_count[key]), "utf8")

    os.write(hist_fd, hist)

def reader(rwsize, r_offset, fname):
    global HEADER
    global PPM_STEP
    global FILLER_B

    global shm
    global empty_sem
    global nonempty_sem

    global rcount
    global r_lock
    global r_condvar

    leftbytes = HEADER["hdr_ops"]["calc_totalbytes"](HEADER)  # la cantidad total de bytes en .ppm sin header
    col_count = {i: 0 for i in range(HEADER["maxcolor"] + 1)}

    out_fname = "h%d-" % (r_offset + 1)
    out_fname += fname

    out_fd = os.open(out_fname, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, stat.S_IWUSR | stat.S_IRUSR)
    os.write(out_fd, HEADER["content"])

    nonempty_sem.acquire()
    while True:

        shm.seek(0, os.SEEK_SET)
        rsize = rwsize if rwsize < leftbytes else leftbytes
        rb = shm.read(rsize)
        wb = bytearray()

        for i in range(0, rsize, PPM_STEP):
            color_int = rb[i + r_offset]
            col_count[color_int] = col_count[color_int] + 1
            color_byte = color_int.to_bytes(1, byteorder="big")
            wb += FILLER_B[:r_offset] + color_byte + FILLER_B[r_offset + 1:]

        os.write(out_fd, wb)
        leftbytes -= len(wb)

        r_lock.acquire()

        rcount.value += 1
        if rcount.value != PPM_STEP:  # se asegura que todos hayan llegado hasta acá antes de seguir
            r_condvar.wait()

        r_condvar.notify()            # si todos señalan solo se pierde la ultima señal ??? jajsjs
        rcount.value -= 1

        if rcount.value == 0:         # el ultimo consumer señala que el buffer puede ser escrito
            empty_sem.release()

        r_lock.release()

        # por que no antes de r_lock?? Para señalar empty_sem y dejarlo en el estado inicial
        if not leftbytes:
            break

        nonempty_sem.acquire()

    os.close(out_fd)

    write_hist(col_count, out_fname)
    sys.stdout.buffer.write(bytes("============== END OF READER %d, left: %d ===============\n" % (r_offset, leftbytes), "utf8"))
    sys.stdout.flush()

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

# =============== Parseo de argumentos y header ================

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

# =============== Main ================

if __name__ == "__main__":
    fname, rwsize = parse_args(sys.argv[1:])

    fd = os.open(fname, os.O_RDONLY)

    shm = mmap.mmap(-1, rwsize)
    empty_sem = mp.Semaphore(1)
    nonempty_sem = mp.Semaphore(0)

    r_lock = mp.Lock()
    r_condvar = mp.Condition(r_lock)
    rcount = mp.sharedctypes.Value('i', 0, lock=False)

    os.lseek(fd, 0, os.SEEK_SET)
    rb = os.read(fd, RSIZE)

    parse_header(rb)

    rwsize = PPM_ALIGN(rwsize)

    for i in range(PPM_STEP):
        p = mp.Process(target=reader, args=(rwsize, i, fname))
        p.start()

    writer(fd, HEADER["f_idx"], rwsize)

    shm.close()
    os.close(fd)
