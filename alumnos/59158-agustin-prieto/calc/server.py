#!/usr/bin/python3
import socket
import argparse
from calculadora import *


def parser():
    parser = argparse.ArgumentParser(description='SERVER SIDE')
    parser.add_argument('-p', '--port', action="store", metavar='PORT', type=int,
                    required=True, help='Port of connection')
    parser.add_argument('-i', '--ip_server', action="store", metavar='IP_SERVER', type=str,
                    required=True)

    args = parser.parse_args()
    return args


def connectToClient(port, ip):
    
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((ip, port))
    serverSocket.listen(5)

    while True:
        conn, addr = serverSocket.accept()
        print(f'CONNECTION TO {addr} SUCCESFUL')

        data = str(conn.recv(1024), encoding='utf-8').split()

        if data[0] == 'suma':
            print('here')
            operacion = suma.delay(data[1], data[2])
            resultado = str(operacion.get(timeout=5))
            conn.send(bytes(resultado, encoding='utf-8'))
            conn.close()

        if data[0] == 'resta':
            operacion = resta.delay(data[1], data[2])
            resultado = str(operacion.get())
            conn.send(bytes(resultado, encoding='utf-8'))
            conn.close()

        if data[0] == 'mult':
            operacion = mult.delay(data[1], data[2])
            resultado = str(operacion.get())
            conn.send(bytes(resultado, encoding='utf-8'))
            conn.close()

        if data[0] == 'div':
            operacion = div.delay(data[1], data[2])
            resultado = str(operacion.get())
            conn.send(bytes(resultado, encoding='utf-8'))
            conn.close()

        if data[0] == 'pot':
            operacion = pot.delay(data[1], data[2])
            resultado = str(operacion.get())
            conn.send(bytes(resultado, encoding='utf-8'))
            conn.close()


if __name__ == '__main__':

    arguments = parser()
    puerto = arguments.port
    ip_addr = arguments.ip_server

    connectToClient(puerto, ip_addr)
