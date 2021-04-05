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
EOF = b""
RWSIZE = 256

# hardcodeo de sizeof(int),
# sys.getsizeof(int) se refiere a int de python q son +400bytes en mi compu jajajsj
PIDSIZE = 4
NCHLD = 2

# entonces python inicializa a 0 la region mmap asi que no hay beneficio de lazy-paging/on-demand paging
# quizas 1MiB es mucho entonces porque es 1MiB a puro page fault, pero bueno hacer algo más dinámico estemmmmm pppppereza
PGSIZE = 4 << 10 # tamaño de página en x86 y x86_64 linux
DMAPSIZE = 1 << 20 # 1MiB en hackerman
CHLDMAPSIZE = PIDSIZE*NCHLD
MMAPSIZE = (DMAPSIZE | CHLDMAPSIZE) & ~(PGSIZE-1)

IOWK_IDX = 0
ROTWK_IDX = 1

# ======================= shm ======================
#   shm se vería así en C
#       struct shm {
#           int siblings[NCHLD];
#           unsigned char data[DMAPSIZE];
#       };
#   por lo tanto:
#       shm + sizeof(int) * NCHLD = data     ó bien en python      shm[CHILDMAPSIZE:] = data
#   y:
#       shm = shm.siblings = siblings        ó bien en python      shm[:CHILDMAPSIZE] = siblings
#
#   en python es posible moverse a offsets puntuales por una zona mapeada usando indexado como si fuera
#   una lista. o bien escribir o leer a partir de un offset predeterminado usando foo.read() o foo.write()
#   es posible llamar foo.seek(IDX, os.SEEK_SET) para asegurar la posición absoluta en la region mmapeada

# debe ser asignado a una region de memoria mmapeada  en algun lugar
# si se reasigna en algun lugar toda la aplicacion ve el cambio asi que kuidao
shm = None

# ======================= IO WORKER ======================

def io_wk():
    global shm
    spid = struct.unpack("II", shm[:CHLDMAPSIZE])[ROTWK_IDX]

    print("Hijo 1 escribiendo...")

    shm.seek(CHLDMAPSIZE, os.SEEK_SET)
    while (rb := os.read(STDIN_NO, RWSIZE)) != EOF:
        shm.write(rb)

    os.kill(spid, signal.SIGUSR1)
    signal.sigwait([signal.SIGUSR1])

    print("Hijo 1 leyendo...")

    shm.seek(CHLDMAPSIZE, os.SEEK_SET)
    sys.stdout.write(shm.read().decode())

    sys.exit(0)

# ======================= ROT WORKER ======================

# @b_arr     bytearray con datos a pasar por rot13
def rot13(b_arr):
    r_alpha = ord("z") - ord("a")
    out = bytearray()
    c = b""

    for b in b_arr:
        if ord("A") <= b and b <= ord("Z"):                 # está en el alfabeto, es mayúscula
            c = (b - ord("A") + 13) % r_alpha + ord("A")
            c = struct.pack("b", c)
        elif ord("a") <= b and b <= ord("z"):               # está en el alfabeto, es minúscula
            c = (b - ord("a") + 13) % r_alpha + ord("a")
            c = struct.pack("b", c)
        else:                                               # no está en el alfabeto, lo pasamos a bytes y dejamos como tal
            c = b.to_bytes(1, byteorder="big")
        out += c
    return out

# ROTCALL sirve para saber si ya se llamó al sighandler de rot_wk
# si rot_wk ejecuta antes que io_wk() entonces signal.pause() aparece en rot_wk()
# si ejecuta después entonces rwk_handler es llamado propiamente al ser un
# sighandler heredado del padre por aparente CLONE_SIGHAND en la implementación de fork de python
ROTCALL = 0

def rwk_handler(signum, frame):
    global ROTCALL
    global shm
    ROTCALL |= 1
    spid = struct.unpack("II", shm[:CHLDMAPSIZE])[IOWK_IDX]
    data = shm[CHLDMAPSIZE:]

    print("Hijo 2 reemplazando...")

    rotted = rot13(data)
    shm.seek(CHLDMAPSIZE, os.SEEK_SET)
    shm.write(rotted)

    os.kill(spid, signal.SIGUSR1)

def rot_wk():
    global ROTCALL

    if not ROTCALL:
        signal.pause()

    sys.exit(0)

# ======================= MAIN ======================

def usage():
    print("Usage: %s -f <path_to_file>" % __file__)

def arg_parse():
    opt, args = getopt.getopt(sys.argv[1:], "f:", "file=")

    if len(opt) < 1 or len(opt[0]) < 2:
        raise ValueError("faltan argumentos")
    fpath = opt[0][1]

    return fpath

if __name__ == "__main__":
    try:
        exitcode = 0
        pidstruct = b""
        fpath = arg_parse()

        shm = mmap.mmap(-1, MMAPSIZE)
        # creo que python no falla en esto pero ni idea no está de más, después leo bien la documentación de mmap
        if not shm:
            raise Exception("No hay suficiente memoria")

        # setear la señal en el padre porque aparentemente hay un CLONE_SIGHAND de por medio en alguna parte del fork.
        # asi que el hijo hereda del padre los sighandlers. con esto me aseguro que aunque el hijo aún no haya
        # corrido va a poder manejar la señal adecuadamente.
        signal.signal(signal.SIGUSR1, rwk_handler)
        rotwk = os.fork()
        if not rotwk:
            rot_wk() # no retorna

        iowk = os.fork()
        if not iowk:
            io_wk() # no retorna

        # python complica mucho compartir estructuras de datos (con clase Manager y eso)
        # yo solo quiero pasar numeros enteros asi que no pienso complicarla (ver shm arriba)
        pidstruct = struct.pack("II", iowk, rotwk)
        shm.write(pidstruct)

        while os.wait():
            continue
    except ChildProcessError as err:
        if err.errno != 10:
            exitcode = 1
    except ValueError as err:
        exitcode = 1
        usage()
    finally:
        if shm:
            shm.close()
        sys.exit(exitcode)
