#!/usr/bin/python3
import pickle
import socket
import argparse
import os

ADDRESS = socket.gethostname()
PORT = 6000
FORMAT = 'utf-8'

parser = argparse.ArgumentParser(description='TP1 - procesa ppm')
parser.add_argument('-l', '--log', action="store", metavar='LOG', type=str,
                    required=True, help='Log File')

args = parser.parse_args()
filename = args.log


log_file = os.open(f'{filename}.txt', os.O_RDWR | os.O_CREAT)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((ADDRESS, PORT))


while True:

    command = input('Command: ')
    print('ok')
    if command == 'exit':
        print('Conexion terminada')
        clientSocket.close()
        break
    to_bytes = pickle.dumps(command)
    clientSocket.send(to_bytes)
    server_message = clientSocket.recv(4096)

    log_line = f'Command: {command}     Output: {server_message}'
    os.write(log_file, log_line.encode())
    
    print(server_message.decode(FORMAT))
