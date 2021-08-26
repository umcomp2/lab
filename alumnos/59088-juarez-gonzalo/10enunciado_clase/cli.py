import sys

from Protocol_CLI import UDP_CLI, TCP_CLI
from cli_parse import parse_args

# funciones independientes del protocolo, send_loop y _send_loop
def _send_loop(frm, to):
    for line in frm:
        to.send(line)

def send_loop(prot):
    _send_loop(sys.stdin, prot)

def main():
    sv_port, t, sv_address = parse_args(sys.argv[1:])
    prot = TCP_CLI(sv_address, sv_port) if t else UDP_CLI(sv_address, sv_port)
    send_loop(prot)
    del prot

if __name__ == "__main__":
    main()
