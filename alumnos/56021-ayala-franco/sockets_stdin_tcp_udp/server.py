from os import O_APPEND, O_CREAT, O_WRONLY
import os
import socket
import argparse
import concurrent.futures
import signal

def lector(socket_cliente: socket.socket):
    datos_cliente = socket_cliente.recv(100)
    os.write(archivo, datos_cliente)
    socket_cliente.shutdown(socket.SHUT_RDWR)

def salir():
    server_socket.shutdown(socket.SHUT_RDWR)
    return 0

signal.signal(signal.SIGINT, salir)

parser = argparse.ArgumentParser()
parser.add_argument("-p", dest="puerto", default=33333)
parser.add_argument("-t", dest="proto", type=str, help="Protocolo de transporte a usar.", choices=("TCP", "UDP"), default="TCP")
parser.add_argument("-f", dest="archivo", type=str, help="Archivo a escribir los datos de los clientes.", default="archivo.txt")

args = parser.parse_args()

pool = concurrent.futures.ThreadPoolExecutor(5)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM if args.proto == "TCP" else socket.SOCK_DGRAM)
server_socket.bind(("127.0.0.1", args.puerto))
server_socket.listen(5)
socket.setdefaulttimeout(10.0)

archivo = os.open(args.archivo, O_CREAT|O_WRONLY|O_APPEND)

while True:
    socket_cliente, addr_info = server_socket.accept()
    pool.submit(lector, socket_cliente)