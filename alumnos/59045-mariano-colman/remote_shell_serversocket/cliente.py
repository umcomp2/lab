from os import PRIO_PGRP
import socket as s
import sys, pickle, time


sCliente = s.socket(s.AF_INET, s.SOCK_STREAM)

host = sys.argv[1]

port = int(sys.argv[2])

sCliente.connect((host, port))
print("[+]CLIENTE CONECTADO!")

pwd = sCliente.recv(1024)
pwd2 = pickle.loads(pwd)

print("[+] Trabajando en el directorio: ", pwd2)

while True:
    coman2 = input(f"\n{pwd2} $> ")
    if not coman2.strip():
        continue
    mensaje = pickle.dumps(coman2)
    sCliente.send(mensaje)
    if coman2.lower() == "exit":
        break

    output = sCliente.recv(2048)
    output2 = pickle.loads(output)

    resultado = output2

    print(resultado)