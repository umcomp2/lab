import socket as s
import argparse, sys

cliente = s.socket(s.AF_INET, s.SOCK_STREAM)

argumentos = argparse.ArgumentParser(description="Cliente juncotic.")
argumentos.add_argument('-a', "--host", type=str, required = True, default="0.0.0.0", help='Host del servidor')
argumentos.add_argument('-p', '--port', type=int, required=True, help='Puerto del servidor')

parseo = argumentos.parse_args()
#HOST = "analytics.juncotic.com"
#HOST = sys.argv[1]
HOST = parseo.host
PORT = parseo.port

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
