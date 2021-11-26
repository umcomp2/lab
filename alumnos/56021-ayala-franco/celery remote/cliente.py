from os import O_APPEND, O_CREAT, O_WRONLY
import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", default="localhost", type=str, help="ip del servidor.")
parser.add_argument("-p", default=51007, type=int, help="puerto del servidor.")
parser.add_argument("-o", choices=('suma', 'rest', 'mult', 'div', 'pot'), help="operacion.")
parser.add_argument("-n", type=float, help="primer operando.")
parser.add_argument("-m", type=float, help="segundo operando.")
args = parser.parse_args()

server = (args.a, args.p)
client_socket = socket.socket()
client_socket.settimeout(2)
try:
    client_socket.connect(server)
except OSError as exception:
    print(exception)
    exit(-1)

client_socket.send(bytes(f"{args.o}:{args.n}:{args.m}", "ASCII"))
r = client_socket.recv(100)
print(r.decode("ASCII"))
client_socket.shutdown(socket.SHUT_RDWR)
exit(0)
