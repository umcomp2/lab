#!/usr/bin/python3

import socket
import sys
import argparse as ap

# parseo de argumentos
parser = ap.ArgumentParser("tcp_udp\n\n")
parser.add_argument('-p', '--port', type=int, help='Puerto de conexion', required=True)
parser.add_argument('-t', type=str, help='Transport protocol [tcp|udp]', required=True)
parser.add_argument('-a', type=str, help='IP del servidor', required=True)
args = parser.parse_args()

server_address = (args.a, args.port)

if (args.t == 'tcp'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Haciendo el connect")
    s.connect(server_address)
    print("Handshake realizado con exito!")
    data = sys.stdin.read()
    print("Enviando datos al server")
    s.send(data.encode())
    print("Datos enviados")
    print("Reciviendo datos del server")
    recv = s.recv(1024)
    print(recv.decode())
    print("Cerrando conexion")
    s.close()

elif (args.t == 'udp'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = sys.stdin.read()
    print("Enviando datos al server")
    s.sendto(data.encode(), server_address)
    print("Reciviendo datos del server")
    server_data, server = s.recvfrom(2048)
    print(server_data.decode())
    print("Cerrando conexion")
    s.close()