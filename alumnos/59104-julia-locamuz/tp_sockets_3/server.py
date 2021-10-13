import socket
import os
import subprocess as sp
from sys import stderr, stdout
import argparse

# Ctrl +D no es una señal, es EOF (EOF). Cierra la tubería stdin. Si read (STDIN)
# devuelve 0, significa stdin cerrado, lo que significa Ctrl + D se golpeó (suponiendo 
# que haya un teclado en el otro extremo de la tubería).



parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-f',help='ruta file', action='store_true')
parser.add_argument('port')
parser.add_argument('-p', action='store_true')
parser.add_argument('protocol')
parser.add_argument('-t', help='protocolo transporte', action='store_true')

args = parser.parse_args()

if args.f: 
    file = args.file

if args.p:
    PORT = int(args.port) # puerto en el que va a atender

if args.t: 
    PROTOCOL = args.protocol # utp/ftp 


#SERVER = socket.gethostbyname(socket.gethostname()) # 'localhost'
# yo quiero que atienda en todas las direcciones
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = b'disconnect\n'


def handle_client_tcp(conn, addr): 
    session = []
    print(f'[NEW CONNECTION] {addr} connected')
    while True:
        msg = conn.recv(1024)
        if msg == DISCONNECT_MSG: 
            print('[DISCONNECT]')
            break
        elif msg == bytes(0): 
            print('[EOF] ---> [DISCONNECT]')
            fd = os.open(file, os.O_CREAT | os.O_RDWR)
            for i in session: 
                os.write(fd, i)
            os.close(fd)
            break
        else: 
            session.append(msg)
        

    conn.close()

def handle_client_udp(server):
    session = []
    while True: 
        msg, addr = server.recvfrom(1024)
        print(f'[NEW MESSAGE] from {addr[0]}')   # address cliente????
        if msg == b'disconnect\n':
            print('[DISCONNECT]')
            break
        elif msg == bytes(0): 
            print('[EOF] ---> [DISCONNECT]')
            fd = os.open(file, os.O_CREAT | os.O_RDWR)
            for i in session: 
                os.write(fd, i)
            os.close(fd)
            break
        else: 
            session.append(msg)


def start():

    print(f'[LISTENING] server is listening on {SERVER}')
    if PROTOCOL == "tcp":
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(ADDR)
        server.listen() 
        while True: 
            conn, addr = server.accept()
            handle_client_tcp(conn, addr)
    elif PROTOCOL == 'udp':         
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(ADDR)
        while True: 
            handle_client_udp(server)
    else: 
        raise ValueError('Protocol not valid')
print("[STARTING] server is starting...")
start()