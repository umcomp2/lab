from os import PRIO_PGRP
import socket as s
import sys, pickle, time


sCliente = s.socket(s.AF_INET, s.SOCK_STREAM)

host = sys.argv[1]

port = int(sys.argv[2])

sCliente.connect((host, port))
print("[+]CLIENTE CONECTADO!")

pwd = sCliente.recv(1024)

print("[+] Trabajando en el directorio: ", pwd.decode())

while True:
    coman2 = input(f"\n{pwd.decode()} $> ")
    if not coman2.strip():
        continue
    sCliente.send(coman2.encode())
    if coman2.lower() == "exit":
        sCliente.close()
        break

    output = sCliente.recv(2048).decode()

    resultado = output

    print(resultado)