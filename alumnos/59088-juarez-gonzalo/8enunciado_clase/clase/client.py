#!/usr/bin/python3

import sys
import socket

BUFFSIZE = 2048
PORT = int(sys.argv[1])

ip_addr = socket.gethostbyname("localhost")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip_addr, PORT))

s.send(b"GET / HTTP/1.1\r\n\r\n")

try:
    rb = 0
    msg = bytearray()
    while (msg := s.recv(BUFFSIZE-rb)):
        rb += len(msg)
        print(msg)
except ConnectionResetError:
    pass

s.close()
