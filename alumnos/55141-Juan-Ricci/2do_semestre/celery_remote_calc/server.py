#!/usr/bin/python3
import socket
import argparse
import celery_calc
# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
"""
    socket.AF_INET -> sockets tcp/ip
    socket.AF_UNIX -> sockets Unix (archivos en disco, similar a FIFO/named pipes)
    socket.SOCK_STREAM -> socket tcp, orientado a la conexion (flujo de datos)
    socket.SOCK_DGRAM -> socket udp, datagrama de usuario (no orientado a la conexion)
"""
# get local machine name
parser = argparse.ArgumentParser(description="Calculadora")
parser.add_argument('-H', '--host', help='IP del host', required=True)
parser.add_argument('-p', '--port', type=int, help='Puerto de conexion', required=True)
args = parser.parse_args()

host = args.host
port = args.port

serversocket.bind((host, port))
serversocket.listen(2)
while True:
    # establish a connection
    print("Esperando conexiones remotas (accept)")
    clientsocket, addr = serversocket.accept()
    print("Got a connection from %s" % str(addr))

    op = clientsocket.recv(1024).decode()
    if (op != ''):
        n = int(clientsocket.recv(1024).decode())
        if (n != ''):
           m = int(clientsocket.recv(1024).decode())

    if (op == 'suma'):
        res = celery_calc.suma.delay(n,m)
    elif (op == 'resta'):
        res = celery_calc.resta.delay(n,m)
    elif (op == 'mult'):
        res = celery_calc.mult.delay(n,m)
    elif (op == 'div'):
        res = celery_calc.div.delay(n,m)
    elif (op == 'pot'):
        res = celery_calc.pot.delay(n,m)

    msg = f'Resultado: {res.get()}'

    clientsocket.send(msg.encode())

    print("Enviando mensaje...")
    # clientsocket.send(res.encode('utf-8'))
    print("Cerrando conexion...")
    clientsocket.close()
