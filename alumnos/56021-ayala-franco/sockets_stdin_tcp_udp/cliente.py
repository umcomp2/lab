import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", dest="server_addr", type=str, help="Dirección del servidor.", default="127.0.0.1")
parser.add_argument("-p", dest="server_port", type=int, help="Puerto a usar.", default=33333)
parser.add_argument("-t", dest="proto", type=str, help="Protocolo de transporte a usar.", choices=("TCP", "UDP"), default="TCP")
args = parser.parse_args()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM if args.proto == "TCP" else socket.SOCK_DGRAM)
server_socket.connect((args.server_addr, args.server_port))

entrada_usuario = ""
try:
    while True:
        entrada_usuario += input()
        entrada_usuario += "\n"
except EOFError:
    # print(entrada_usuario)
    server_socket.send(entrada_usuario.encode("ASCII"))
finally:
    server_socket.shutdown(socket.SHUT_RDWR)