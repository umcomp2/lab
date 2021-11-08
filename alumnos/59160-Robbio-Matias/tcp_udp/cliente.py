import socket
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address',action="store",default='127.0.0.1', type= str)
parser.add_argument('-p', '--port',action="store", type= int, required=True)
parser.add_argument('-t', '--tprotocol',action="store",choices=['tcp','udp'], required=True, type=str)
args = parser.parse_args()

ADDR = args.address
PORT = args.port
PROTOCOL = args.tprotocol

if PROTOCOL == 'tcp':
    cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cliente.connect((ADDR,PORT))
elif PROTOCOL == 'udp':
    cliente = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    

while True:
    msg = str(input()+'\n')

    if PROTOCOL == 'tcp':
        cliente.send(msg.encode('utf-8'))
        cliente.recv(4096)
    elif PROTOCOL == 'udp':
        cliente.sendto(msg.encode('utf-8'),(ADDR, PORT))
    
    if msg == "":
        break
        
cliente.close()
print("Finalizando conexion")
