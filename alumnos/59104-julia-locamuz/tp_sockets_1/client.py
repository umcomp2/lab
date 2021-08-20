import socket

# Los sockets stream se basa en el protocolo TCP, que es un protocolo orientado a conexión

PORT = 5050
SERVER = '127.0.1.1' 
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = 'disconnect'

client = socket.socket()
client.connect(ADDR)

def send(): 
    input1 = input('command: ')
    message = input1.encode(FORMAT)
    client.send(message)

while True: 
    send()