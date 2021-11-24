import socket as s
import threading, pickle, os, time, subprocess, signal, argparse
from sys import stderr, stdout, stdin


parser = argparse.ArgumentParser(description="Servidor TCP-UDP")
parser.add_argument('-p', '--port', type=int, default=1000, help='Puerto del servidor')
parser.add_argument('-t', '--type', type=str, default='TCP', help='Tipo de protocolo a utilizar')
parser.add_argument('-f', '--file', type=str, help='Ruta del archivo')

argu = parser.parse_args()

if argu.type == 'TCP':
    servidor = s.socket(s.AF_INET, s.SOCK_STREAM)
else:
    servidor = s.socket(s.AF_INET, s.SOCK_DGRAM)
servidor.getsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

HOST = '0.0.0.0'
PORT = argu.port
TYPE = argu.type
SEPARATOR = "sep"
parametro = servidor

servidor.bind((HOST, PORT))

print("[+]SERVIDOR INICIADO!")

#TCP conexion
if argu.type == 'TCP':
    servidor.listen()
    socketCliente, addr = servidor.accept()
    parametro = socketCliente
    print("[+]CONEXION ESTABLECIDA DE {}:{}".format(addr[0], addr[1]))
    parametro.send(TYPE.encode())

#UDP recive msj
if argu.type == 'UDP':
    data, addr = parametro.recvfrom(1024)
    print(f'UPD establecido {data.decode()}')
    parametro.sendto(TYPE.encode(), addr)
lista = []
while True:
    mensaje = parametro.recv(1024)
    if mensaje != bytes(0):
        print("Mensaje recibido:", mensaje.decode())
    if mensaje.decode() == 'exit':
        print("Cliente desconectado")
        break
    elif mensaje == bytes(0):
        print("EOF")
        fd = os.open(argu.file ,os.O_RDWR|os.O_CREAT)
        for i in lista:
            os.write(fd, i)
            os.write(fd, b'\n')
        os.close(fd)
        break
    else:
        lista.append(mensaje)

