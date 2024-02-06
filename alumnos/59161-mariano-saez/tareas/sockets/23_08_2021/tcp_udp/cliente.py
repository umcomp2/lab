import argparse
import socket
import os


STDIN = 0

def start(TYPE):
    s = socket.socket(socket.AF_INET, TYPE)
    return s

def tcp(sock_cli, ADDR, PORT):
    # Conectar al server
    sock_cli.connect((ADDR, PORT))

    while True:
        data = os.read(STDIN, 4096)
        sock_cli.send(data)
        if data.decode() == "":
            break
        sock_cli.recv(4096)

def udp(sock_cli, ADDR, PORT):
    while True:
        data = os.read(STDIN, 4096)
        sock_cli.sendto(data, (ADDR, PORT))
        if data.decode() == "":
            break


if __name__ == "__main__":

    # Obtener por CLI [SERVER] y [PORT]
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", type=str, default="127.0.0.1", help="Server IP")
    parser.add_argument("-p", "--port", type=int, help="Server PORT")
    parser.add_argument("-t", "--type", type=str, default="tcp", help="Protocolo de transporte")
    args = parser.parse_args()

    ADDR = args.address
    PORT = args.port
    if args.type == "tcp":
        TYPE = socket.SOCK_STREAM
    else:
        TYPE = socket.SOCK_DGRAM

    s = start(TYPE)
    print("\nIniciando cliente con los siguiente parametros:")
    print(f"\tDireccion destino: {ADDR}")
    print(f"\tPuerto destino: {PORT}")
    print(f"\tProtocolo: {args.type.upper()}\n")

    if TYPE == "tcp":
        tcp(s, ADDR, PORT)
    else:
        udp(s, ADDR, PORT)

    print("Finalizando conexion...")
    s.close()
    exit(0)


