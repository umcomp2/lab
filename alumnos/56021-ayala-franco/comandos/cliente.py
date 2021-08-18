from os import O_APPEND, O_CREAT, O_WRONLY
import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l")
args = parser.parse_args()

server = ("127.0.0.1", 51007)
client_socket = socket.socket()
try:
    client_socket.connect(server)
except OSError as exception:
    print(exception)
    client_socket.shutdown(socket.SHUT_RDWR)
    exit(-1)

if args.l:
    file = open(args.l, "w+")

while (command := input("> ")) != ".exit":
    client_socket.send(bytes(command, "utf-8"))
    answer = client_socket.recv(1000)
    if file:
        file.write(str(answer, "utf-8") + str("\n"))
    print(str(answer, "utf-8"))

client_socket.shutdown(socket.SHUT_RDWR)
exit(0)