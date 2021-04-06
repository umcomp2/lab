#!/usr/bin/env python3

import os
import sys
import signal
import mmap
import struct

import getopt

RWSIZE = 256
STDIN_NO = 0

maponymous = None
MMAPSIZE = 1 << 20

def usagendie():
    print("Usage: %s -f <path_to_file>" % __file__)
    sys.exit(1)

# ======================= IO WORKER =======================

def iowk_SIGUSR1_handler(signum, frame):
    global maponymous
    maponymous.seek(0, os.SEEK_SET)
    sys.stdout.buffer.write(maponymous.read())
    os._exit(os.EX_OK)

def io_worker():
    global maponymous
    rb = b""
    while (rb := os.read(STDIN_NO, RWSIZE)) != b"":
        maponymous.write(rb)

    os.kill(os.getppid(), signal.SIGUSR1)
    signal.pause()

# ======================= ROT WORKER =======================

def rot13(bstr):
    alpha_r = ord("z") - ord("a")
    out = bytearray()
    c = b""

    for b in bstr:
        if ord("A") <= b and b <= ord("Z"):
            c = (b - ord("A") + 13) % alpha_r + ord("A")
            c = struct.pack("b", c)
        elif ord("a") <= b and b <= ord("z"):
            c = (b - ord("A") + 13) % alpha_r + ord("a")
            c = struct.pack("b", c)
        else:
            c = b.to_bytes(1, byteorder="big")
        out += c
    return out

def rotwk_SIGUSR1_handler(signum, frame):
    global maponymous
    rotted = rot13(maponymous.read())
    maponymous.seek(0, os.SEEK_SET)
    maponymous.write(rotted)
    os.kill(os.getppid(), signal.SIGUSR2)
    print("rot handler")
    os._exit(os.EX_OK)


def rot_worker():
    signal.pause()

# ======================= "PARENT" =======================

# se pierde la señal si se ejecuta el handler antes que pid_rot
def prnt_SIGUSR1_handler(signum, frame):
    global pid_rot
    os.kill(pid_rot, signal.SIGUSR1)

def prnt_SIGUSR2_handler(signum, frame):
    global pid_io
    os.kill(pid_io, signal.SIGUSR1)

if __name__ == "__main__":
    try:
        opt, args = getopt.getopt(sys.argv[1:], "f:", "file=")
        if len(opt) < 1 or len(opt[0]) < 2:
            raise ValueError("faltan argumentos")
        fpath = opt[0][1]

        maponymous = mmap.mmap(-1, MMAPSIZE)
        signal.signal(signal.SIGUSR2, prnt_SIGUSR2_handler)
        signal.signal(signal.SIGUSR1, prnt_SIGUSR1_handler)

        pid_io = os.fork()
        if not pid_io:
            signal.signal(signal.SIGUSR1, iowk_SIGUSR1_handler)
            io_worker()

        pid_rot = os.fork()
        if not pid_rot:
            signal.signal(signal.SIGUSR1, rotwk_SIGUSR1_handler)
            rot_worker()

        while os.wait():
            continue
    except ChildProcessError as err:
        if err.errno == 10:
            print("exit status de procesos hijos recolectado")
        else:
            raise
    except ValueError as err:
        if str(err) == "faltan argumentos":
            usagendie()
        raise
