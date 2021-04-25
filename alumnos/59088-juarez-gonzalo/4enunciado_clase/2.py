#!/usr/bin/env python3
import os
import sys
import stat
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
STDOUT_NO = 1
EOF = b""
RWSIZE = 256

# hardcodeo de sizeof(int),
# sys.getsizeof(int) se refiere a int de python q son 416bytes en mi compu jajajsj
PIDSIZE = 4
NCHLD = 2
CHLDMAPSIZE = PIDSIZE*NCHLD

IOWK_IDX = 0
ROTWK_IDX = 1

# debe ser asignado a una region de memoria mmapeada  en algun lugar
# si se reasigna en algun lugar toda la aplicacion ve el cambio asi que kuidao
packedpids = None

# ======================= IO WORKER ======================

def io_wk():
    global fpath
    global packedpids
    spid = struct.unpack("II", packedpids[:CHLDMAPSIZE])[ROTWK_IDX]

    print("Hijo 1 escribiendo...")

    fd = os.open(fpath, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, stat.S_IRUSR | stat.S_IWUSR)

    while (rb := os.read(STDIN_NO, RWSIZE)) != EOF:
        os.write(fd, rb)

    os.close(fd)

    os.kill(spid, signal.SIGUSR1)
    signal.sigwait([signal.SIGUSR1])

    print("Hijo 1 leyendo...")

    fd = os.open(fpath, os.O_RDONLY)

    while (rb := os.read(fd, RWSIZE)) != EOF:
        os.write(STDOUT_NO, rb)

    os.close(fd)

    sys.exit(0)

# ======================= ROT WORKER ======================

# @b_arr     bytearray con datos a pasar por rot13
def rot13(b_arr):
    r_alpha = ord("z") - ord("a") + 1
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
# sighandler heredado del padre por aparente CLONE_SIGHAND en la implementación de fork
ROTCALL = 0

def rwk_handler(signum, frame):
    global ROTCALL
    global fpath
    global packedpids
    ROTCALL |= 1
    spid = struct.unpack("II", packedpids[:CHLDMAPSIZE])[IOWK_IDX]

    print("Hijo 2 reemplazando...")

    fd = os.open(fpath, os.O_RDWR)

    pos = 0
    while (rb := os.read(fd, RWSIZE)) != EOF:
        rotted = rot13(rb)
        os.lseek(fd, pos, os.SEEK_SET)
        os.write(fd, rotted)
        pos += len(rb)

    os.close(fd)
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

        packedpids = mmap.mmap(-1, CHLDMAPSIZE)
        # creo que python no falla en esto pero ni idea no está de más, después leo bien la documentación de mmap
        if not packedpids:
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
        # yo solo quiero pasar numeros enteros asi que no pienso complicarla
        pidstruct = struct.pack("II", iowk, rotwk)
        packedpids.write(pidstruct)

        while os.wait():
            continue
    except ChildProcessError as err:
        if err.errno != 10:
            exitcode = 1
    except ValueError as err:
        exitcode = 1
        usage()
    finally:
        if packedpids:
            packedpids.close()
        sys.exit(exitcode)
