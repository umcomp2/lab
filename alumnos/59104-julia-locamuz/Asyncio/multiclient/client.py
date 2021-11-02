import pickle
import socket
import argparse
import os

ADDRESS = 'localhost'
PORT = 8888
FORMAT = 'utf-8'

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--log', action="store", type=str,
                    required=True)

args = parser.parse_args()


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((ADDRESS, PORT))


while True:

    command = input('Command: ')
    if command == 'exit':
        print('Conexion terminada')
        break

    print('OK')
    
    to_bytes = pickle.dumps(command)
    clientSocket.send(to_bytes)
    
    server_response = clientSocket.recv(4096)
    server_response = pickle.loads(server_response)


clientSocket.close()