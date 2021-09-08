import argparse
import socket
import threading
import os
import sys


parser = argparse.ArgumentParser(description="Datos servidor")
parser.add_argument("-p","--port", dest="port", type = int, required = True, help ="Puerto en el que atiende el servidor")
parser.add_argument("-t","--protocol", dest="protocol", required = True, help = "Protocolo a utilizar")
parser.add_argument("-f","--file", dest="file", required = True, help = "Archivo de texto en blanco")

args = parser.parse_args()
protocolo = args.protocol


SERVER = ""
DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = "utf-8"

if protocolo == "tcp":

    PORT = args.port
    ADDR = (SERVER, PORT)
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server.bind(ADDR)

if protocolo == "udp":

    PORT = args.port
    ADDR = (SERVER, PORT)
    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server.bind(ADDR)


def handle_client(conn, addr):

    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        pid_hilo = threading.get_ident()
        pid = os.getpid()
        msg = conn.recv(1024)

        if msg != bytes(0):
            archivo = open(args.file + ".txt", "ab")
            archivo.write(msg + bytes("--->", FORMAT) +  bytes(f"From process: {pid}, Hilo: {pid_hilo}\n", FORMAT))
            archivo.close()

        elif msg == bytes(0):
            print(f"Proceso: {pid}, Hilo: {pid_hilo} ---> Disconnect")
            break
    conn.close()


def handle_client_udp():
    data, adress = server.recvfrom(1024)
    print(f"[NEW CONNECTION] {adress}  connected.")
    connected = True
    while connected:
        pid = os.getpid()
        if data != bytes(0):
            archivo = open(args.file + ".txt", "ab")
            archivo.write(data + bytes("--->", FORMAT) +  bytes(f"From process: {pid}\n", FORMAT))
            archivo.close()

        elif data == bytes(0):
            print(f"Proceso: {pid} ---> Disconnect")
            sys.exit()
            break
    



def start():
    
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        
        if protocolo == "tcp":
            server.listen()
            conn, addr = server.accept()        
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
        elif protocolo == "udp":
            handle_client_udp()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()