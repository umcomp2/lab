import socket as s
import sys, os, subprocess


sCliente = s.socket(s.AF_INET, s.SOCK_STREAM)

host = sys.argv[1]

port = int(sys.argv[2])

sCliente.connect((host, port))

pwd = sCliente.recv(1024)
#HABILITAR AMBOS SI SE UTILIZA SERVERFORK
#msj = sCliente.recv(1024)
#print("Hola cliente: {}".format(msj.decode()))

print("[+] Trabajando en el directorio: ", pwd.decode())

while True:
    coman2 = input(f"\n{pwd.decode()} $> ")
    if not coman2.strip():
        continue
    sCliente.send(coman2.encode())
    if coman2.lower() == "exit":
        break

    output = sCliente.recv(2048).decode()

    resultado, directorio = output.split("<sep>")

    print(resultado)