#!/usr/bin/env python3
import os
import stat
import sys
import getopt

import multiprocessing as mp
from multiprocessing.sharedctypes import Value
import mmap

# ================ Ayuda general a lo largo del programa ================

EOF = b""

INIT_RSIZE = 512            # tamaño de lectura inicial (usado para leer el header)

INFONL = 3                  # total de lineas del header que aportan info en .ppm

B_PER_PX = 3                # cantidad de bytes que conforman un pixel en .ppm
NCHILD = B_PER_PX           # cantidad de hijos (NOTA: valor igual a B_PER_PX, legibilidad no)
NPROD = NCHILD              # cantidad de producers (NOTA: idem nota NCHILD)

FILLER_B = b"\x00\x00\x00"  # usada para extraer bytes nulos, len(FILLER_B) == B_PER_PX

# Alinea un numero contra B_PER_PX, B_PER_PX no es potencia de 2 asi que no bitwise :(
# @size:    tamaño numerico
def PPM_ALIGN(size):
    global B_PER_PX
    return size // B_PER_PX * B_PER_PX if size >= B_PER_PX else B_PER_PX

# Transforma un numero representado en un bytearray al datatype Number
#   Eg.: b"\x32\x35\x35" -> 255
# @b_arr:   representacion de numero en bytearray.
def btoi(b_arr):
    ret = 0
    for i in range(len(b_arr)):
        ret = ret * 10 + (b_arr[i] - ord('0'))
    return ret

# =============== Diccionario para header y funciones correspondientes ================
# Header sin comentarios es de la forma: MAGIC\nCOLS ROWS\nMAX_BYTE_VAL\n
# La cantidad de bytes a leer sin el header como:
#               COLS * ROWS * 3 * (MAX_BYTE_VAL+1) >> 8

# NOTA: Podría ser una clase pero el resto del código no es OO
#       y para no mezclar la cuestión meh use referencia a objetos,
#       y que las funciones son objetos en python para algo parecido
#       al OO en C con un struct con punteros a funciones (virtual table?).
#       Use diccionario en lugar de struct, que es mas bien una hash table
#       pero bueno es lo que hay. Al menos el tiempo de acceso teoricamente es O(1) (?

# Calcula la cantidad de bytes necesarios para el maximo valor
# posible en un color de archivo .ppm
# @header:  diccionario hdr
def h_calc_colorsize(header):
    return (header["maxcolor"] + 1) >> 8

# Calcula la cantidad total de bytes (sin header) que hay en un archivo .ppm
# @header:  diccionario hdr
def h_calc_totalbytes(header):
    global B_PER_PX
    return header["hdr_ops"]["calc_colorsize"](header) * B_PER_PX * header["cols"] * header["rows"]

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
    "hdr_ops": hdr_ops
}

# =============== Sincronizacion sobre la memoria compartida ================
#   Sincronizacion necesaria en algoritmo producer-consumer estandar

shm = None          # el buffer compartido
empty_sem = None    # shm esta vacio
nonempty_sem = None # shm tiene contenido

# =============== Sincronizacion sobre consumers ===============
#   Un consumer que haya terminado con el bloque A,
#   no puede empezar a leer un bloque B sin esperar a que el resto
#   de los consumers haya terminado de leer el bloque A

pcount = 0         # indica la cantidad de consumers que ya terminaron de leer shm
p_lock = None      # lock sobre variable pcount
p_condvar = None   # variable condicional que trabaja con read_lock

# =============== Algoritmo  ================
# Producer-Consumer modificado para sincronizar lectura de bloques entre consumers
# Nota: Producer es el proceso padre de los hijos

# Escribe el histograma que corresponde a la consigna
# @col_count:   Diccionario con la cantidad de apariciones de un color mapeadas al valor numerico de ese color en el .ppm
def write_hist(col_count, fname):
    hist = bytearray()      # si esto fuera a parar al stack entonces es media nefasta la cuestion. pero es python
    hist_fname = fname + ".hist"
    hist_fd = os.open(hist_fname, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, stat.S_IWUSR | stat.S_IRUSR)

    for key in col_count.keys():
        hist += bytes("%d:\t%d\n" % (key, col_count[key]), "utf8")

    os.write(hist_fd, hist)
    os.close(hist_fd)

# @rwsize:      Cantidad de bytes a leer indicadas por input del usuario
# @r_offset:    Offset del color que corresponde a este consumer
# @fname:       Nombre del archivo original
def consumer(rwsize, r_offset, fname):
    global B_PER_PX
    global NPROD
    global FILLER_B

    global hdr

    global shm
    global empty_sem
    global nonempty_sem

    global pcount
    global p_lock
    global p_condvar

    leftbytes = hdr["hdr_ops"]["calc_totalbytes"](hdr)
    col_count = {i: 0 for i in range(hdr["maxcolor"] + 1)}

    out_fname = "h%d-" % (r_offset + 1)
    out_fname += fname

    out_fd = os.open(out_fname, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, stat.S_IWUSR | stat.S_IRUSR)
    os.write(out_fd, hdr["content"])

    nonempty_sem.acquire()
    while True:

        shm.seek(0, os.SEEK_SET)
        rsize = rwsize if rwsize < leftbytes else leftbytes
        rb = shm.read(rsize)
        wb = bytearray()

        for i in range(0, rsize, B_PER_PX):
            color_int = rb[i + r_offset]
            col_count[color_int] = col_count[color_int] + 1
            color_byte = color_int.to_bytes(1, byteorder="big")
            wb += FILLER_B[:r_offset] + color_byte + FILLER_B[r_offset + 1:]

        os.write(out_fd, wb)
        leftbytes -= len(wb)

        ### COMIENZO DE MODIFICACION AL PRODUCER-CONSUMER ESTANDAR ###
        p_lock.acquire()

        pcount.value += 1
        if pcount.value != NPROD:  # se asegura que todos hayan llegado hasta acá antes de seguir
            p_condvar.wait()

        pcount.value -= 1

        if pcount.value == 0:         # el ultimo consumer señala semaforo de buffer vacio (para producer)
            empty_sem.release()

        p_condvar.notify()            # si todos señalan solo se pierde la ultima señal ??? jajsjs
        p_lock.release()
        ### FIN DE MODIFICACION AL PRODUCER-CONSUMER ESTANDAR ###

        # por que no antes de p_lock?? Para señalar empty_sem y dejarlo en el estado inicial
        if not leftbytes:
            break

        nonempty_sem.acquire()

    os.close(out_fd)
    write_hist(col_count, out_fname)

# @fd:          file descriptor del archivo siendo leído
# @rwsize:      Cantidad de bytes a leer indicadas por input del usuario
def producer(fd, rwsize):
    global EOF
    global NPROD

    global hdr

    global shm
    global empty_sem
    global nonempty_sem

    rb = b""
    b_count = 0

    os.lseek(fd, hdr["f_idx"], os.SEEK_SET) # comenzar lectura en 1er byte post-header
    while (rb := os.read(fd, rwsize)) != EOF:
        b_count += len(rb)
        empty_sem.acquire()         # buffer vacio (y/o consumido), escribir

        shm.seek(0, os.SEEK_SET)
        shm.write(rb)

        for i in range(NPROD):
            nonempty_sem.release()  # buffer con contenido, señalar para consumers

# =============== Parseo de argumentos y header ================

def usagendie():
    h = "usage: %s [-h] (-s|--size) SIZE (-f|--file) FILE\n\n" % __file__
    h += "TP1 - procesa ppm\n\n"
    h += "\t-h, --help\tMuestra esta ayuda\n"
    h += "\t-s, --size\tTamaño del bloque de lectura\n"
    h += "\t-f, --file\tArchivo a procesar\n"
    sys.stdout.write(h)
    sys.exit(0)

# @argv:    Lista de argumentos
def parse_args(argv):
    opt, args = getopt.getopt(argv, "s:f:h", ["size=", "file=", "help"])
    fname = ""
    rwsize = 0

    for o in opt:
        oname = o[0].replace("-","")
        if oname[0] == "s":
            rwsize = int(o[1])
        elif oname[0] == "f":
            fname = o[1]
        elif oname[0] == "h":
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
    global hdr

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
        raise ValueError("Demasiados comentarios en el header, header superior a %d bytes" % INIT_RSIZE)

    hdr_fields = hdr_no_cmmnt.split(b'\n')

    hdr["content"] = rb[:f_idx]
    hdr["f_idx"] = f_idx

    hdr["magic"] = hdr_fields[0].decode()

    hdr["cols"], hdr["rows"] = hdr_fields[1].split(b" ")
    hdr["cols"] = btoi(hdr["cols"])
    hdr["rows"] = btoi(hdr["rows"])

    hdr["maxcolor"] = btoi(hdr_fields[2])

# =============== Main ================

if __name__ == "__main__":
    fname, rwsize = parse_args(sys.argv[1:])

    fd = os.open(fname, os.O_RDONLY)

    rwsize = PPM_ALIGN(rwsize)

    shm = mmap.mmap(-1, rwsize)
    empty_sem = mp.Semaphore(1)
    nonempty_sem = mp.Semaphore(0)

    p_lock = mp.Lock()
    p_condvar = mp.Condition(p_lock)
    pcount = mp.sharedctypes.Value('i', 0, lock=False)

    os.lseek(fd, 0, os.SEEK_SET)
    rb = os.read(fd, INIT_RSIZE)

    parse_header(rb)


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
