#!/usr/bin/python3
import socket
import argparse



IP = socket.gethostname()
EOF = b''


def parser():
    parser = argparse.ArgumentParser(description='Connection to juncotic')
    parser.add_argument('-a', '--address', action="store", metavar='ADDRESS', type=str,
                    required=True, help='Server IP addr')
    parser.add_argument('-p', '--port', action="store", metavar='PORT', type=int,
                    required=True, help='Port of connection')
    parser.add_argument('-t', '--transport', action="store", metavar='TRANSPORT', type=str,
                    required=True, help='Transport Protocol')
    

    args = parser.parse_args()
    return args



def connectToServer(protocol, port, ip):
    if protocol == 'tcp':
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((ip, port))
        print(f'CONNECTION TO SERVER ON {ip} SUCCESFUL')


        while True:
            try:
                chunk = input('Ingrese una cadena de texto: ')
            except EOFError:
                # clientSocket.send(b'done')
                clientSocket.close()
                break
            message = bytes(chunk, 'utf-8') +b'\n'
            clientSocket.send(message)


    if protocol == 'udp':
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            try:
                chunk = input('Ingrese una cadena de texto: ')
            except EOFError:
                # clientSocket.send(b'done')
                clientSocket.close()
                break
            message = bytes(chunk, 'utf-8') +b'\n'
            clientSocket.sendto(message, (ip, port))


if __name__ == '__main__':
    arguments = parser()
    protocolo = arguments.transport
    puerto = arguments.port
    addr = arguments.address

    connectToServer(protocolo, puerto, addr)



