import socket
from typing import Counter
import argparse

ADDRESS = socket.gethostname()

parser = argparse.ArgumentParser(description='Connection to juncotic')
parser.add_argument('-p', '--port', action="store", metavar='PORT', type=int,
                    required=True, help='Port of connection')

args = parser.parse_args()
PORT = args.port

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((ADDRESS, PORT))

def get_input():
    command = (input('')).encode('ascii')
    clientSocket.send(command)
    sv_response = clientSocket.recv(4096)
    return sv_response

count = 0
while True:

    
    if count == 4:
        clientSocket.close()
        break

    sv_response = get_input().decode('ascii')
    
    if sv_response == '200':
        count += 1
    elif sv_response == '400':
        print('Comando válido, pero fuera de secuencia.')
    elif sv_response == '500':
        print('Comando inválido.')
    elif sv_response == '404':
        print('Clave errónea.')
    elif sv_response == '405':
        print('Cadena nula.')

