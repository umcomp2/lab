#!/usr/bin/python3
import socket
import ssl

import subprocess as sp
import threading as tr

# already synchronized queue (python3+)
from queue import Queue

from common import *

NTHREADS = 64

PORT = 8080
HOSTNAME = ""
BACKLOGSIZE = NTHREADS

tr_pool = [None]*NTHREADS
conn_q = None

def run_cmd(cmd):
    return sp.run(
            cmd,
            shell=True,
            stdout=sp.PIPE,
            stderr=sp.STDOUT,
            encoding="utf8")

#p = {
#        returncode : int
#        stdout : bytes
#        args : str
#    }
# python3 "stderr=sp.STDOUT" == bash "2>&1"
# sp.PIPE (docs): "Special value that can be used as the stdin, stdout
# or stderr argument to Popen and indicates that a pipe to the
# standard stream should be opened."
def shell_loop(s):
    while cmd := recv_msg(s):
        if (cmd == "exit"):
            print("EXITING")
            break
        p = run_cmd(cmd)
        msg = ""
        if p.returncode != 0:
            msg += "ERROR. RETCODE %d" % p.returncode
        else:
            msg += "OK. RETCODE: %d" % p.returncode
        msg += "\n\n" + p.stdout
        send_msg(s, msg)
    s.close()

def pool_loop():
    global conn_q

    s, addr = conn_q.get()
    shell_loop(s)


def start_tr_pool():
    for i in range(NTHREADS):
        tr_pool[i] = tr.Thread(target=pool_loop, args=())
        tr_pool[i].start()

def ssl_sv_wrap(sv_s):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('./certificado.pem', './clave.pem')
    return context.wrap_socket(sv_s, server_side=True)

def set_tcp_sv():
    sv_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sv_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR | socket.SO_REUSEPORT, 1)
    sv_s.bind((HOSTNAME, PORT))
    sv_s.listen(BACKLOGSIZE)
    return sv_s

def main():
    global conn_q

    sv_s = set_tcp_sv()
    sv_s = ssl_sv_wrap(sv_s)
    conn_q = Queue()
    start_tr_pool()
    while True:
        conn = sv_s.accept()
        conn_q.put(conn)

if __name__ == "__main__":
    main()