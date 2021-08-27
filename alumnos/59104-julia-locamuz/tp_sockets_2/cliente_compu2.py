import socket
from datetime import datetime

PORT = 2222
SERVER = '127.0.1.1' 
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'


client = socket.socket()
client.connect(ADDR)
connected = True

while connected == True:
    input1 = input()
    if input1 == 'exit':
        connected = False
    msg = input1.encode(FORMAT)
    client.send(msg)
    respuesta = client.recv(1024).decode()
    print('\n',respuesta)

