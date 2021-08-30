import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", help="Host")
parser.add_argument("-p", help="Port", type=int)
args = parser.parse_args()

server_socket = socket.socket()
server_socket.connect((args.t, args.p))

comandos = ["hello", "email", "key"]

for comando in comandos:
    respuesta = ""
    while "200" not in respuesta:
        entrada = input("Ingrese " + comando + ": ")
        server_socket.send(bytes(comando + "|" + entrada, "ascii"))
        respuesta = str(server_socket.recv(100), "ascii")
        print(respuesta)
server_socket.send(b"exit")
print(str(server_socket.recv(100), "ascii"))
print(str(server_socket.recv(100), "ascii"))
