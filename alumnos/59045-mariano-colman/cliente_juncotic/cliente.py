import socket as s
import os, sys

cliente = s.socket(s.AF_INET, s.SOCK_STREAM)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

cliente.connect((HOST, PORT))

while True:
    name = "hello|{}".format(input(f"\nIngrese su nombre: "))
    cliente.send(name.encode())
    status = cliente.recv(1024)
    print(status.decode())
    email = "email|{}".format(input(f"\nIngrese su email: "))
    cliente.send(email.encode())
    status = cliente.recv(1024)
    print(status.decode())
    key = "key|{}".format(input(f"\nIngrese su clave: "))
    cliente.send(key.encode())
    status = cliente.recv(1024)
    print(status.decode())
    cliente.send(input(f"Ingrese exit para finalizar: ").encode())
    status = cliente.recv(1024)
    print(status.decode())
    cliente.close()
    break
