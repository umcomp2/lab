import socket
from datetime import datetime
import pickle

PORT = 5050
SERVER = '127.0.1.1' 
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = 'disconnect'

#session = server_fork0.session

client = socket.socket()
client.connect(ADDR)

while True:
    input1 = input('command: ')
    # msg = input1.encode(FORMAT)
    input1_ser = pickle.dumps(input1)
    client.send(input1_ser)
    if input1 == DISCONNECT_MSG: 
        print('[DISCONNECT]')
        break
    respuesta = client.recv(1024)
    respuesta_des = pickle.loads(respuesta)
    print('\n',respuesta_des.decode())
