from os import O_APPEND, O_CREAT, O_WRONLY
import socket
import argparse
import pickle
import signal

def salir(uno, dos):
    client_socket.shutdown(socket.SHUT_RDWR)
    print("CONTROL+C...")
    exit(0)

signal.signal(signal.SIGINT, salir)

parser = argparse.ArgumentParser()
parser.add_argument("-l")
args = parser.parse_args()

server = ("127.0.0.1", 57001)
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
    deserialized_answer = pickle.loads(answer)
    result = f"=== Execution Result: {str(deserialized_answer.returncode)} ===\n{deserialized_answer.stdout}=== Execution End ==="
    if args.l:
        file.write(str(result, "utf-8") + str("\n"))
    print(result)

client_socket.close()
exit(0)