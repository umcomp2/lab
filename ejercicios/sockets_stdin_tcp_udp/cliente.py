import socket 
import argparse
import sys
parser = argparse.ArgumentParser(description='SOCKET TCP/UDP')
parser.add_argument('-i', '--ip', dest = "ip", required = True, help = "IP Utilizada")
parser.add_argument('-p', '--port', dest = "port", type = int, required = True, help = "Puerto Utilizado")
parser.add_argument('-t', '--tipo', dest = "tipo", required = True, help = "Protocolo Utilizado")
args = parser.parse_args()

PROTOCOLO = args.tipo
SERVIDOR = "0.0.0.0"
PORT = args.port
ADDR  = (SERVIDOR, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "\n---DESCONECTADO---" 

if PROTOCOLO == "tcp":
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ClientSocket.connect(ADDR)

    for i in sys.stdin:
        ClientSocket.send(i.encode(FORMAT))
    
    ClientSocket.send("DESCONECTADO".encode(FORMAT))
    ClientSocket.close()

elif PROTOCOLO == "udp":
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in sys.stdin:
        if i != DISCONNECT_MESSAGE:
            ClientSocket.sendto(i.encode(FORMAT), ADDR)
        else:
            print("DESCONECTADO")

    ClientSocket.sendto("DESCONECTADO".encode(FORMAT), ADDR)
    ClientSocket.close()


