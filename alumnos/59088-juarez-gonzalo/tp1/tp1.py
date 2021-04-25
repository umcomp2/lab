#!/usr/bin/env python3
import os
import stat
import sys
import getopt

import multiprocessing as mp
from multiprocessing.sharedctypes import Value
import mmap

# ================ MISC ================

EOF = b""

INIT_RSIZE = 512            # tamaño de lectura inicial (usado para leer el header)

INFONL = 3                  # total de lineas del header que aportan info en .ppm

NCOLORS = 3                 # cantidad de colores
NCHILD = NCOLORS            # cantidad de hijos (NOTA: valor igual a NCOLORS, legibilidad no)
NCONSUM = NCOLORS           # cantidad de producers (NOTA: idem nota NCHILD)

def PPM_ALIGN(num, b_per_px):
    return num // b_per_px * b_per_px if num >= b_per_px else b_per_px

# @b_arr:   bytearray
def btoi(b_arr):
    ret = 0
    for i in range(len(b_arr)):
        ret = ret * 10 + (b_arr[i] - ord('0'))
    return ret

# =============== hdr ================
#
# Header sin comentarios es de la forma:
#                MAGIC\nCOLS ROWS\nMAX_BYTE_VAL\n

# @header:  diccionario hdr
def h_calc_colorsize(header):
    maxval = header["maxcolor"]
    if maxval & 0xff00:
        return 2
    return 1

# @header:  diccionario hdr
def h_calc_totalbytes(header):
    return header["hdr_ops"]["calc_colorsize"](header) * header["b_per_px"] * header["cols"] * header["rows"]

hdr_ops = {
    "calc_totalbytes": h_calc_totalbytes,
    "calc_colorsize": h_calc_colorsize,
}

hdr = {
    "content": "",
    "f_idx": "",

    "magic": "",
    "cols": 0,
    "rows": 0,

    "maxcolor": 0,
    "b_per_px": 0,
    "b_per_color": 0,
    "filler_b": b"",

    "hdr_ops": hdr_ops,
}

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

# =============== PRODUCER-CONSUMER ================
#
#   NOTA: Producer es proceso padre de consumers

# @color_count:   diccionario con la cantidad de apariciones de un color mapeadas al valor numerico de ese color en el .ppm
def write_hist(color_count, fname):
    hist = bytearray()
    hist_fname = fname + ".hist"
    hist_fd = os.open(hist_fname, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, stat.S_IWUSR | stat.S_IRUSR)

    for key in color_count.keys():
        hist += b"%d:\t%d\n" % (int.from_bytes(key, byteorder="big"), color_count[key])

    os.write(hist_fd, hist)
    os.close(hist_fd)

def empty_sem_up():
    global empty_sem
    empty_sem.release()

# @rwsize:      cantidad de bytes a leer indicadas por input del usuario
# @c_offset:    offset del color que corresponde a este consumer, sus valores van de 0-2 (r, g, b)
# @fname:       nombre del archivo original
def consumer(rwsize, c_offset, fname):
    global hdr

    global shm
    global empty_sem
    global nonempty_sem

    global c_barrier

    out_fname = "h%d-" % (c_offset + 1)
    out_fname += fname

    out_fd = os.open(out_fname, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, stat.S_IWUSR | stat.S_IRUSR)
    os.write(out_fd, hdr["content"])

    leftbytes = hdr["hdr_ops"]["calc_totalbytes"](hdr)
    color_count = {}
    for i in range(hdr["maxcolor"] + 1):
        key = i.to_bytes(hdr["b_per_color"], byteorder="big")
        color_count[key] = 0

    s_offset = c_offset * hdr["b_per_color"]
    e_offset = s_offset + hdr["b_per_color"]

    while leftbytes:
        nonempty_sem.acquire()

        n = rwsize if rwsize < leftbytes else leftbytes
        shm.seek(0, os.SEEK_SET)
        rb = shm.read(n)
        wb = bytearray()

        for i in range(0, n, hdr["b_per_px"]):
            color_byte = rb[i + s_offset: i + e_offset]

            color_count[color_byte] = color_count[color_byte] + 1
            wb += hdr["filler_b"][:s_offset] + color_byte + hdr["filler_b"][e_offset:]

        os.write(out_fd, wb)
        leftbytes -= len(wb)

        # llama empty_sem_up() 1 cuando todos los producers terminan .wait()
        c_barrier.wait()

    os.close(out_fd)
    write_hist(color_count, out_fname)

# @fd:          file descriptor del archivo siendo leído
# @rwsize:      cantidad de bytes a leer indicadas por input del usuario
def producer(fd, rwsize):
    global EOF
    global NCONSUM

    global hdr

    global shm
    global empty_sem
    global nonempty_sem

    rb = b""

    # leer a partir del 1er byte post-header
    os.lseek(fd, hdr["f_idx"], os.SEEK_SET)
    while (rb := os.read(fd, rwsize)) != EOF:
        empty_sem.acquire()

        shm.seek(0, os.SEEK_SET)
        shm.write(rb)

        for i in range(NCONSUM):
            nonempty_sem.release()

# =============== PARSE ARGS & HEADER ================

def usagendie():
    h = "usage: %s [-h] (-s|--size) SIZE (-f|--file) FILE\n\n" % __file__
    h += "TP1 - procesa ppm\n\n"
    h += "\t-h, --help\tMuestra esta ayuda\n"
    h += "\t-s, --size\tTamaño del bloque de lectura\n"
    h += "\t-f, --file\tArchivo a procesar\n"
    sys.stdout.write(h)
    sys.exit(0)

# @argv:    lista de argumentos
def parse_args(argv):
    opt, args = getopt.getopt(argv, "s:f:", ["size=", "file="])
    fname = ""
    rwsize = 0

    for o in opt:
        oname = o[0].replace("-","")

        if oname[0] == "s":
            rwsize = int(o[1])
            continue

        if oname[0] == "f":
            fname = o[1]
            continue

        usagendie()

    if not fname or not rwsize:
        raise ValueError("Faltan parametros")

    # super mega validacion de formato de archivo
    if ".ppm" != fname[-4:]:
        raise ValueError("Archivo no tiene extensión ppm")

    return fname, rwsize

# Parsea el header de un archivo .ppm, populando el diccionario hdr global con informacion
# @rb:  Bytes donde se encuentra el header
def parse_header(rb):
    global INFONL
    global NCOLORS
    global hdr

    hdr_no_cmmnt = bytearray()
    nls = 0         # contador de '\n' en lineas que aportan info
    f_idx = 0       # indice posterior al ultimo newline de linea que aporta info
    in_cmmnt = 0    # flag que indica si prox '\n' corresponde a linea de comentario
    c = b""

    for i in range(len(rb)):

        if rb[i] == ord('#'):
            in_cmmnt |= 1
            continue

        if rb[i] == ord('\n') and in_cmmnt:
            in_cmmnt &= 0
            continue

        if rb[i] == ord('\n'):
            nls += 1

        if not in_cmmnt:
            hdr_no_cmmnt += rb[i].to_bytes(1, byteorder="big")

        if nls == INFONL:
            f_idx = i + 1
            break

    if nls != INFONL:
        raise ValueError("Demasiados comentarios en el header, header superior a %d bytes" % INIT_RSIZE)

    hdr_fields = hdr_no_cmmnt.split(b'\n')
    hdr["content"] = rb[:f_idx]
    hdr["f_idx"] = f_idx
    hdr["magic"] = hdr_fields[0]

    hdr["cols"], hdr["rows"] = hdr_fields[1].split(b" ")
    hdr["cols"] = btoi(hdr["cols"])
    hdr["rows"] = btoi(hdr["rows"])
    hdr["maxcolor"] = btoi(hdr_fields[2])

    hdr["b_per_px"] = hdr["hdr_ops"]["calc_colorsize"](hdr) * NCOLORS
    hdr["b_per_color"] = hdr["b_per_px"] // NCOLORS
    hdr["filler_b"] = b"\x00" * hdr["b_per_px"]

# =============== MAIN ================

if __name__ == "__main__":
    fname, rwsize = parse_args(sys.argv[1:])

    fd = os.open(fname, os.O_RDONLY)
    rb = os.read(fd, INIT_RSIZE)
    parse_header(rb)

    rwsize = PPM_ALIGN(rwsize, hdr["b_per_px"])

    shm = mmap.mmap(-1, rwsize)
    empty_sem = mp.Semaphore(1)
    nonempty_sem = mp.Semaphore(0)

    c_barrier = mp.Barrier(NCHILD, empty_sem_up)


    pool = []
    for i in range(NCHILD):
        pool.append(mp.Process(target=consumer, args=(rwsize, i, fname)))
        pool[i].start()

    producer(fd, rwsize)

    for p in pool:
        p.join()

    sys.stdout.write("- Lo logré?\n- Lo logró Señor\n\n\tSe generaron correctamente %d histogramas\n" % NCHILD)

    shm.close()
    os.close(fd)
