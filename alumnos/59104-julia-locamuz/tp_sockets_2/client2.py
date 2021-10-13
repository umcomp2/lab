import socket
import argparse_l
from datetime import datetime

PORT = 5050
SERVER = '127.0.1.1' 
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = 'disconnect'
FILE = argparse_l.file
#session = server_fork0.session


client = socket.socket()
client.connect(ADDR)

file = open(FILE, 'w')

while True:
    input1 = input('command: ')
    msg = input1.encode(FORMAT)
    client.send(msg)
    if input1 == DISCONNECT_MSG: 
        print('[DISCONNECT]')
        break
    respuesta = client.recv(1024).decode()
    print('\n',respuesta)
    file.write(str(ADDR)+'\n'+respuesta+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n\n')
