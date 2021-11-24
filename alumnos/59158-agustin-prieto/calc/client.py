#!/usr/bin/python3
import socket
import argparse



def parser():
    parser = argparse.ArgumentParser(description='SERVER SIDE')
    parser.add_argument('-p', '--port', action="store", metavar='PORT', type=int,
                    required=True, help='Port of connection')
    parser.add_argument('-i', '--ip_server', action="store", metavar='IP_SERVER', type=str,
                    required=True)
    parser.add_argument('-o', '--operacion', action="store", metavar='OPERACION', type=str,
                    required=True, choices=['suma', 'resta', 'mult', 'div', 'pot'])

    parser.add_argument('-n', '--n', action="store", metavar='PRIMER_OP', type=int,
                    required=True)
    parser.add_argument('-m', '--m', action="store", metavar='SEGUNDO_OP', type=int,
                    required=True)

    args = parser.parse_args()
    return args

def connectToServer(op, port, ip, n, m):

    message = bytes(f"{op} {n} {m}", encoding="utf-8")
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((ip, port))
    print(f'CONNECTION TO SERVER ON {ip} SUCCESFUL')
    clientSocket.send(message)
    result = clientSocket.recv(1024)
    print(str(result,encoding="utf-8"))


if __name__ == '__main__':
    arguments = parser()
    op = arguments.operacion
    puerto = arguments.port
    addr = arguments.ip_server
    n1 = arguments.n
    n2 = arguments.m

    connectToServer(op, puerto, addr, n1, n2)
    