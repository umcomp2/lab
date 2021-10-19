import argparse
import sys
import socket

# Manejo de argumentos
parser = argparse.ArgumentParser(description= "Socket TCP-UDP")
parser.add_argument("-i", "--ip", dest = "ip", required = True, help ="ip del servidor a conectarse")
parser.add_argument("-p","--port", dest="port", type = int, required = True, help ="Puerto en el que atiende el servidor")
parser.add_argument("-t","--protocol", dest="protocol", required = True, help = "Protocolo a utilizar")

args = parser.parse_args()
protocolo = args.protocol

PORT = args.port
SERVER = args.ip
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

if protocolo == "tcp":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    for i in sys.stdin:
        client.send(i.encode(FORMAT))
        if i.strip() == bytes(0):
            print("[DISCONNECT]")
            break

if protocolo == "udp":
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.connect(ADDR)
    for i in sys.stdin:
        client.sendto(i.encode(FORMAT),ADDR)
        if i.strip() == DISCONNECT_MESSAGE:
            print("[DISCONNECT]")
            sys.exit()
    client.send(bytes(0), FORMAT)