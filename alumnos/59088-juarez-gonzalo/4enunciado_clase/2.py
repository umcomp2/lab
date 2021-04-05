#!/usr/bin/env python3
import os
import sys
import signal

import mmap
import struct

import getopt

# 2 - Mediante señales, comunique a dos procesos hijos para que:
# El hijo1 cree el archivo indicado con el argumento --file y escriba en el todo lo que le llega por stdin.
# Una vez que termine de escribir, el hijo 2 debe abrir el archivo, y reemplazar todos los caracteres algoritmo rot-13 de cifrado.
# Finalmente, el hijo 1 debe abrir nuevamente el archivo solo lectura y enviar su contenido por stdout.
#
# Ejemplo de funcionamiento
#
# echo "CONTENIDO DEL ARCHIVO"| ./2.py --file archivo
# hijo1 escribiendo ...
# hijo2 reemplazando ..
# hijo1 leyendo .......
# PBAGRAVQB QRY NEPUVIB

STDIN_NO = 0
RWSIZE = 256

# hardcodeo de sizeof(int),
# sys.getsizeof(int) se refiere a int de python q son +400bytes en mi compu jajajsj
PIDSIZE = 4
NCHLD = 2
CHLDMAPSIZE = PIDSIZE*NCHLD

DMAPSIZE = 1 << 20 # 1MiB en hackerman

IOWK_IDX = 0
ROTWK_IDX = 1

# ======================= mmaped_struct ======================
#   el mmaped_struct se vería así en C
#       struct mmaped_struct {
#           int siblings[NCHLD];
#           unsigned char data[DMAPSIZE];
#       };
#   por lo tanto
#   mmaped_struct + sizeof(int) * NCHLD = data     ó bien en python      mmaped_struct[CHILDMAPSIZE:] = data

mmaped_struct = None # debe ser mapeado en main

# ======================= IO WORKER ======================

def io_wk():
    global mmaped_struct
    spid = struct.unpack("II", mmaped_struct[:CHLDMAPSIZE])[ROTWK_IDX]

    print("Hijo 1 escribiendo...")

    mmaped_struct.seek(CHLDMAPSIZE, os.SEEK_SET)
    while (rb := os.read(STDIN_NO, RWSIZE)) != b"":
        mmaped_struct.write(rb)

    os.kill(spid, signal.SIGUSR1)
    signal.sigwait([signal.SIGUSR1])
    print("Hijo 1 leyendo...")

    mmaped_struct.seek(CHLDMAPSIZE, os.SEEK_SET)
    sys.stdout.write(mmaped_struct.read().decode())

    sys.exit(0)

# ======================= ROT WORKER ======================

ROTCALL = 0

# @b_arr     bytearray con datos a pasar por rot13
def rot13(b_arr):
    r_alpha = ord("z") - ord("a")
    out = bytearray()
    c = b""

    for b in b_arr:
        if ord("A") <= b and b <= ord("Z"):
            c = (b - ord("A") + 13) % r_alpha + ord("A")
            c = struct.pack("b", c)
        elif ord("a") <= b and b <= ord("z"):
            c = (b - ord("A") + 13) % r_alpha + ord("a")
            c = struct.pack("b", c)
        else:
            c = b.to_bytes(1, byteorder="big")
        out += c
    return out


def rwk_handler(signum, frame):
    print("Hijo 2 reemplazando...")
    global ROTCALL
    global mmaped_struct
    ROTCALL |= 1
    spid = struct.unpack("II", mmaped_struct[:CHLDMAPSIZE])[IOWK_IDX]
    data = mmaped_struct[CHLDMAPSIZE:]

    rotted = rot13(data)
    mmaped_struct.seek(CHLDMAPSIZE, os.SEEK_SET)
    mmaped_struct.write(rotted)

    os.kill(spid, signal.SIGUSR1)

def rot_wk():
    global ROTCALL

    if not ROTCALL:
        signal.pause()

    sys.exit(0)

# ======================= MAIN ======================

def arg_parse():
    opt, args = getopt.getopt(sys.argv[1:], "f:", "file=")

    if len(opt) < 1 or len(opt[0]) < 2:
        raise ValueError("faltan argumentos")
    fpath = opt[0][1]

    return fpath

if __name__ == "__main__":
    try:
        fpath = arg_parse()
        pidstruct = b""

        mmaped_struct = mmap.mmap(-1, CHLDMAPSIZE + DMAPSIZE)
        # creo que python no falla en esto pero ni idea no está de más, después leo bien la documentación de mmap
        if not mmaped_struct:
            raise Exception("No hay suficiente memoria")

        signal.signal(signal.SIGUSR1, rwk_handler)
        rotwk = os.fork()
        if not rotwk:
            rot_wk() # no retorna

        iowk = os.fork()
        if not iowk:
            io_wk() # no retorna

        # python complica mucho compartir estructuras de datos (con clase Manager y eso)
        # yo solo quiero pasar numeros enteros asi que no pienso complicarla
        pidstruct = struct.pack("II", iowk, rotwk)
        mmaped_struct.write(pidstruct)

        while os.wait():
            continue
    except ChildProcessError as err:
        if err.errno == 10:
            pass
    finally:
        if mmaped_struct:
            mmaped_struct.close()
        sys.exit(0)
