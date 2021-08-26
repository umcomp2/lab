import sys
import os

import getopt

from Protocol_SV import TCP_SV, UDP_SV

# funciones independientes del protocolo, recv_loop y _recv_loop
def _recv_loop(frm, to): # (from, to) pero from es keyword reservada
    r = ""
    while r := frm.recv():
        to.write(r)

def recv_loop(prot, filepath):
    with open(filepath, "w") as f:
        _recv_loop(prot, f)

def parse_args(args):
    opts, args = getopt.getopt(args, "p:t:f:")
    port = 8080     # port:     default 8080
    t = 1           # tcp:      default 1 ("tcp")
    filepath = ""   # filepath: no default
    for opt in opts:
        if opt[0] == "-p":
            port = int(opt[1])
        if opt[0] == "-t":
            t = 1 if opt[1] == "tcp" else 0
        if opt[0] == "-f":
            filepath = opt[1]

    if not filepath or os.path.isfile(filepath):
        raise ValueError("Error en el archivo especificado %s" % filepath)

    return (port, t, filepath)

def main():
    port, t, filepath = parse_args(sys.argv[1:])
    prot = TCP_SV(port) if t else UDP_SV(port)
    recv_loop(prot, filepath)
    del prot

if __name__ == "__main__":
    main()
