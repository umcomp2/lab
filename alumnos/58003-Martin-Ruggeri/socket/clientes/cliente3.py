#!/usr/bin/python3
import socket
import os
import sys

sockete_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
# host = socket.gethostname()
host = sys.argv[1]
port = int(sys.argv[2])

print("connection to hostname on the port")
sockete_cliente.connect((host, port))
# este connect maxea con el accept del servidor ahi se hace el sin sin ac ac
print("Handshake successful connection")
# receive no more than 1024 bytes
print("waiting for data from server")
msg = sockete_cliente.recv(1024)
print(msg.decode('utf-8'))
sockete_cliente.close()
print("closing connection!")
