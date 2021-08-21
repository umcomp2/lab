#!/usr/bin/python3
import socket

PORT = 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", PORT))

s.listen(5)

(conn_s, addr) = s.accept()
conn_s.send(b"PUTO EL Q LEA\r\n")
conn_s.close()
s.close()
