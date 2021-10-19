#!/usr/bin/python3

import socket
import sys
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
print(s)

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

print("Haciendo el connect")
s.connect((host, port))   
print("Handshake realizado con exito!")

while True:
    command = input("Ingrese el comando a ejecutar: ")
    print("Enviando datos al server")
    msg = pickle.dumps(command)
    s.send(msg)
    if command == "exit":
        break

    print("Reciviendo datos del server")
    new_recv = s.recv(1024)
    recv = pickle.loads(new_recv)
    print(recv.decode())
    if (len(sys.argv) > 1):
        if (arg1 == "-l"):
            log = open(arg2, "a")
            log.write(recv.decode())
            log.close()

s.close()
print("Cerrando conexion")
