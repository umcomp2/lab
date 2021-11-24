import socket as s
from sys import stderr, stdout, stdin
import os, signal, argparse

parseo = argparse.ArgumentParser(description="Cliente TCP-UDP")
parseo.add_argument('-a', '--address', type=str, default='0.0.0.0', help='Direccion del servidor')
parseo.add_argument('-p', '--port', type=int, default=1000, help='Puerto del servidor')
parseo.add_argument('-t', '--type', type=str, default='TCP', help='Protocolo a utilizar')

argu = parseo.parse_args()
#signal.signal(signal.SIGUSR1, handler)

if argu.type.upper() == 'TCP':
    cliente = s.socket(s.AF_INET, s.SOCK_STREAM)
else:
    cliente = s.socket(s.AF_INET, s.SOCK_DGRAM)

host = argu.address

port = argu.port

#Cliente TCP - Conexion
if argu.type.upper() == 'TCP':
    cliente.connect((host, port))
    print("[+]CLIENTE CONECTADO!")
    pwd = cliente.recv(1024)

#Cliente UDP - STR Connect
if argu.type.upper() == 'UDP':
    print("[+]CLIENTE CONECTADO!")
    msj = "String conexion"
    cliente.sendto(msj.encode(), (host, port))
    pwd = cliente.recv(1024)


print("Servidor utilizando protocolo",pwd.decode())
for i in stdin:
    if argu.type.upper() == 'TCP':
        cliente.send(i.strip().encode())
    else:
        cliente.sendto(i.strip().encode(), (host, port))
    if i.strip() == 'exit':
        print("Desconectado")
        break
cliente.sendto(''.encode(), (host, port))
cliente.close()

