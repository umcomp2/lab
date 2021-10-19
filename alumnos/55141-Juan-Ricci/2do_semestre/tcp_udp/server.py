#!/usr/bin/python3
import socket, sys, time
import subprocess as sp
import argparse as ap
"""
    socket.AF_INET -> sockets tcp/ip
    socket.AF_UNIX -> sockets Unix (archivos en disco, similar a FIFO/named pipes)
    socket.SOCK_STREAM -> socket tcp, orientado a la conexion (flujo de datos)
    socket.SOCK_DGRAM -> socket udp, datagrama de usuario (no orientado a la conexion)
"""

# parseo de argumentos
parser = ap.ArgumentParser("tcp_udp\n\n")
parser.add_argument('-p', '--port', type=int, help='Puerto de conexion', required=True)
parser.add_argument('-t', type=str, help='Transport protocol [tcp|udp]', required=True)
parser.add_argument('-f', '--file', action='store', type=str, help='Ruta a archivo de texto')
args = parser.parse_args()

file = open(args.file, 'w')

def connect(puerto):
    host = "0.0.0.0"     
    port = puerto
    serversocket.bind((host, port))       

if (args.t == 'tcp'):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connect(args.port)
    serversocket.listen(2)
    while True:
        print("Esperando conexiones remotas (accept)")
        clientsocket, addr = serversocket.accept()      
        print("Got a connection from %s" % str(addr))
        client_data = clientsocket.recv(1024)
        file.write(client_data.decode())
        file.close()
        print("Enviando confirmacion al cliente...")
        confirm = f"Archivo {args.file} escrito!"
        clientsocket.send(confirm.encode())
        print("Esperando un tiempito...")
        time.sleep(3)
        print("Cerrando conexion...")
        clientsocket.close()

    
elif (args.t == 'udp'):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   
    connect(args.port)
    while True:
        print("Reciviendo mensaje del cliente...")
        data, address = serversocket.recvfrom(2048)
        print("Mensaje recivido.")
        print(f"Escribiendo mensaje en {args.file}...")
        file.write(data.decode())
        file.close()
        print("Enviando confirmacion al cliente...")
        confirm = f"Archivo {args.file} escrito!"
        serversocket.sendto(confirm.encode(), address)
        print("Esperando un tiempito...")
        time.sleep(3)