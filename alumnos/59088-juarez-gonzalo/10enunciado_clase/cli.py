import sys
import socket

import getopt
import re

from Protocol_CLI import UDP_CLI, TCP_CLI

# funciones independientes del protocolo, send_loop y _send_loop
def _send_loop(frm, to):
    for line in frm:
        to.send(line)

def send_loop(prot):
    _send_loop(sys.stdin, prot)

# robado de -> https://www.ipregex.com/ porque me dio flojera hacer un buen regex de ip
re_address = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
def parse_args(args):
    opts, args = getopt.getopt(args, "p:t:a:")
    sv_port = 8080      # sv_port:     default 8080
    t = 1               # tcp:      default 1 ("tcp")
    sv_address = ""     # sv_address:  no default
    for opt in opts:
        if opt[0] == "-p":
            sv_port = int(opt[1])
        if opt[0] == "-t":
            t = 1 if opt[1] == "tcp" else 0
        if opt[0] == "-a":
            sv_address = opt[1]

    if not sv_address or not re_address.match(sv_address):
        raise ValueError("Error en la dirección especificada %s" % sv_address)

    return (sv_port, t, sv_address)

def main():
    sv_port, t, sv_address = parse_args(sys.argv[1:])
    prot = TCP_CLI(sv_address, sv_port) if t else UDP_CLI(sv_address, sv_port)
    send_loop(prot)
    del prot

if __name__ == "__main__":
    main()
