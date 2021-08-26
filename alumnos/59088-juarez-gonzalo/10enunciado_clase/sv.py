import sys

from Protocol_SV import TCP_SV, UDP_SV
from sv_parse import parse_args

# funciones independientes del protocolo, recv_loop y _recv_loop
def _recv_loop(frm, to): # (from, to) pero from es keyword reservada
    r = ""
    while r := frm.recv():
        to.write(r)

def recv_loop(prot, filepath):
    with open(filepath, "w") as f:
        _recv_loop(prot, f)

def main():
    port, t, filepath = parse_args(sys.argv[1:])
    prot = TCP_SV(port) if t else UDP_SV(port)
    recv_loop(prot, filepath)
    del prot

if __name__ == "__main__":
    main()
