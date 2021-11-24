#!/usr/bin/python3

import socket
import argparse
import os


hostname = socket.gethostname()
IP = "0.0.0.0"
print(f'Server IP address: {IP}')
EOF = b''
END_MSG = b'done'


def createFile(fd):
    newFile =os.open(f'{fd}.txt', os.O_RDWR | os.O_CREAT)
    return newFile


def parser():
    parser = argparse.ArgumentParser(description='SERVER SIDE')
    parser.add_argument('-p', '--port', action="store", metavar='PORT', type=int,
                    required=True, help='Port of connection')
    parser.add_argument('-t', '--transport', action="store", metavar='TRANSPORT', type=str,
                    required=True, help='Transport Protocol')
    parser.add_argument('-f', '--file', action="store", metavar='FILE', type=str,
                    required=True, help='File path')

    args = parser.parse_args()
    return args


def connectToClient(protocol, port, file, ip=IP):


    if protocol == 'tcp':
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((ip, port))
        serverSocket.listen(5)

        conn, addr = serverSocket.accept()
        print(f'CONNECTION TO {addr} SUCCESFUL')

        while True:
            chunk = conn.recv(10)
            if chunk == EOF:
                serverSocket.close()
                print('SERVER CLOSED')
                break
            os.write(file, chunk)


    if protocol == 'udp':
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind((ip, port))
        while True:
            chunk, addr = serverSocket.recvfrom(4096)
            if chunk == END_MSG:
                serverSocket.close()
                print('SERVER CLOSED')
                break
            os.write(file, chunk)


if __name__ == '__main__':

    arguments = parser()
    puerto = arguments.port
    protocolo = arguments.transport
    path = arguments.file

    txt = createFile(path)

    connectToClient(protocolo, puerto, txt)

    exit

