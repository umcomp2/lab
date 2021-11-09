#!/usr/bin/python3

import socket
import argparse
import time

# parseo de argumentos
parser = argparse.ArgumentParser(description="Calculadora")
parser.add_argument('-H', '--host', help='IP del host', required=True)
parser.add_argument('-p', '--port', type=int, help='Puerto de conexion', required=True)
parser.add_argument('-o', '--operation', type=str, help='Operacion matematica a realizar (suma, resta, mult, div, pot)', required=True)
parser.add_argument('-n', type=int, help='Puerto de conexion', required=True)
parser.add_argument('-m', type=int, help='Puerto de conexion', required=True)
args = parser.parse_args()

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
print(s)

# get address
host = args.host
port = args.port

# get operation
op = args.operation
n = args.n
m = args.m

print("Haciendo el connect")
# connection to hostname on the port.
s.connect((host, port))   
print("Handshake realizado con exito!")

print("Enviando operacion al servidor")
s.send(op.encode())
time.sleep(0.5)
print("Enviando primer operando al servidor")
s.send(str(n).encode())
time.sleep(0.5)
print("Enviando segundo operando al servidor")
s.send(str(m).encode())
time.sleep(0.5)

print("Reciviendo datos del server")
recv = s.recv(1024)
print(recv.decode())

#print (msg.decode('ascii'))
#print (msg.decode('utf-8'))
s.close()
print("Cerrando conexion")