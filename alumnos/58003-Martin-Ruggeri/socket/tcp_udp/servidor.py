#!/usr/bin/python3
import socket
import argparse


def parser_socket():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="Puerto en el que atendera el server",)
    parser.add_argument("-t", "--type", type=str, help="Protocolo de capa de transporte TCP/UDP", default="tcp")
    parser.add_argument("-f", "--file", type=str, help="Ruta de archivo en el que escribir", default="/dev/null")
    return parser.parse_args()


def start_socket(type_socket, TYPE, PORT, FILE):
    '''El parámetro socket_type, especifica el tipo de socket que se creará.
    SOCK_STREAM indica que los datos pasan a través del socket como una secuencia de caracteres.
    SOCK_DGRAM indica que los datos estarán en forma de datagramas.'''
    # Crear, bindear y poner a escuchar el server
    s = socket.socket(socket.AF_INET, type_socket)
    s.bind(("0.0.0.0", PORT))
    # Crear archivo (si no existe antes)
    f = open(f"{FILE}", "w+")
    if TYPE == "tcp":
        tcp(s,f)
    else:
        udp(s,f)
    return s, f


def tcp(s, f):
    s.listen()
    conn, addr = s.accept()
    print(f"Iniciando conexion con {addr}...")

    while True:
        data = conn.recv(4096).decode()
        f.write(data)
        f.flush()
        if data == "":
            print(f"Finalizando conexion con {addr}...")
            conn.close()
            break
        conn.send(b"ACK") # Para habilitar a que envie nuevamente


def udp(s, f):
    while True:
        data, addr = s.recvfrom(4096)
        f.write(data.decode())
        f.flush()

        if data.decode() == "":
            print(f"Finalizando conexion con {addr}...")
            break



if __name__ == "__main__":
    # Obtener los parametros por CLI
    args = parser_socket()
    PORT = args.port
    FILE = args.file
    TYPE = args.type
    if TYPE == "tcp":
        type_socket = socket.SOCK_STREAM
    elif TYPE == "udp":
        type_socket = socket.SOCK_DGRAM
    else:
        print("ingreso mal el tipo de cumnicacion")
        exit(0)

    print("\nServidor iniciado con los siguiente parametros:")
    print(f"\tPuerto: {PORT}")
    print(f"\tProtocolo: {TYPE}")
    print(f"\tArchivo destino: {FILE}\n")
    s, f = start_socket(type_socket, TYPE, PORT, FILE)

    print("Cerrando servidor...")
    f.close()
    s.close()
    exit(0)
