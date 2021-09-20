#!/usr/bin/python3
import argparse
import socket
import os


def parser_socket():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", type=str, default="127.0.0.1", help="Server IP")
    parser.add_argument("-p", "--port", type=int, help="Server PORT")
    parser.add_argument("-t", "--type", type=str, default="tcp", help="Protocolo de transporte")
    return parser.parse_args()


def start_socket(type_socket, TYPE, ADDR, PORT, STDIN):
    s = socket.socket(socket.AF_INET, type_socket)
    if TYPE == "tcp":
        tcp(s, ADDR, PORT, STDIN)
    else:
        udp(s, ADDR, PORT, STDIN)
    return s

def tcp(sock_cli, ADDR, PORT, STDIN):
    # Conectar al server
    sock_cli.connect((ADDR, PORT))

    while True:
        data = os.read(STDIN, 4096)
        sock_cli.send(data)
        if data.decode() == "":
            break
        sock_cli.recv(4096)

def udp(sock_cli, ADDR, PORT, STDIN):
    while True:
        data = os.read(STDIN, 4096)
        sock_cli.sendto(data, (ADDR, PORT))
        if data.decode() == "":
            break


if __name__ == "__main__":
    # Obtener por CLI [SERVER] y [PORT]
    args = parser_socket()
    ADDR = args.address
    PORT = args.port
    TYPE = args.type
    STDIN = 0
    if TYPE == "tcp":
        type_socket = socket.SOCK_STREAM
    elif TYPE == "udp":
        type_socket = socket.SOCK_DGRAM
    else :
        print("Ingresaste mal el tipo de comunicacion")
        exit(0)

    print("\nIniciando cliente con los siguiente parametros:")
    print(f"\tDireccion destino: {ADDR}")
    print(f"\tPuerto destino: {PORT}")
    print(f"\tProtocolo: {TYPE}\n")

    s = start_socket(type_socket, TYPE, ADDR, PORT, STDIN)

    print("Finalizando conexion...")
    s.close()
    exit(0)
