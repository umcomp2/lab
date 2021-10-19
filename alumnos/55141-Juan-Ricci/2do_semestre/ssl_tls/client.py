#!/usr/bin/python3

import socket
import sys
import pickle
import ssl

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket!')
    sys.exit()  

if (len(sys.argv) > 1):
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    if (arg1 == "-l"):
        log = open(arg2, "w")
        log.close()
    else:
        print("Usage: -l [file] to save log")

host = socket.gethostname()
port = 1234

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.verify_mode = ssl.CERT_REQUIRED
#context.check_hostname = True
context.load_default_certs()

print("Haciendo el connect")
ssl_sock = context.wrap_socket(s, server_hostname=host)
ssl_sock.connect((host, port))
print("Handshake realizado con exito!")

while True:
    command = input("Ingrese el comando a ejecutar: ")
    print("Enviando datos al server")
    msg = pickle.dumps(command)
    ssl_sock.send(msg)
    if command == "exit":
        break

    print("Reciviendo datos del server")
    new_recv = ssl_sock.recv(1024)
    recv = pickle.loads(new_recv)
    print(recv.decode())
    if (len(sys.argv) > 1):
        if (arg1 == "-l"):
            log = open(arg2, "a")
            log.write(recv.decode())
            log.close()

ssl_sock.close()
print("Cerrando conexion")
