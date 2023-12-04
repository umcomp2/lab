from os import close
import socket
import threading
import argparse

parser = argparse.ArgumentParser(description= 'SOCKET TCP/UDP')
parser.add_argument('-p','--port', dest = "port", type = int, required= True, help = "Puerto Utilizado" )
parser.add_argument('-t','--protocolo', dest = "protocolo", type = str, required= True, help = "Protocolo Utilizado" )
parser.add_argument('-f','--file', dest = "file", type = str, required= True, help = "Archivo Utilizado" )
args = parser.parse_args()

PROTOCOLO = args.protocolo
SERVIDOR = "0.0.0.0"
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "\n---DESCONECTADO---" 

if PROTOCOLO == "udp":
    PORT = args.port
    ADDR = (SERVIDOR, PORT)
    ServerSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    ServerSocket.bind(ADDR)


elif PROTOCOLO == "tcp":
    PORT = args.port
    ADDR = (SERVIDOR, PORT)
    ServerSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ServerSocket.bind(ADDR)


def handle_client_tcp(conn, addr):
    print(f"---NUEVA CONEXIÓN---\n {addr} conectado con exito.")
    while True:
        msg = conn.recv(1024)
        if msg != "DESCONECTADO":
            archivo = open(args.file + ".txt", "ab")
            archivo.write(msg, FORMAT)
            archivo.close()
        else:
            print(DISCONNECT_MESSAGE)
            break
    conn.close()
def handle_client_udp():
    while True:
        a, b = ServerSocket.recvfrom(4096)
        if a != "DESCONECTADO":
            archivo = open(args.file + ".txt", "ab")
            archivo.write(a)
        else:
            print(DISCONNECT_MESSAGE)
            break

def start():
    if PROTOCOLO == "tcp":
        print("--PROTOCOLO TCP--")
        ServerSocket.listen()
        conn, addr = ServerSocket.accept()
        thread = threading.Thread(target=handle_client_tcp, args=(conn, addr))
        thread.start()
    if PROTOCOLO == "udp":
        handle_client_udp()

print("---STARTING--- El servidor ha comenzado...")
start()
    



            


