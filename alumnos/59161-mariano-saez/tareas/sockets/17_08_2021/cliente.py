import socket
import argparse


# Datos del cliente
datagram = {
    "hello" : None,
    "email" : None,
    "key": None,
}

parser = argparse.ArgumentParser()
parser.add_argument("-host", type=str, help="Server IP addr")
parser.add_argument("-port", type=int, help="Server port")
args = parser.parse_args()

HOST = args.host
PORT = args.port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Conexion exitosa!")

for i in datagram:
    datagram[i] = input(f"Ingrese {i}: ")

for i in datagram:
    s.send(bytes(f"{i}|{datagram[i]}", "utf-8"))
    code = str(s.recv(128), "utf-8")
    while code != "200":
        print(f"{i} incorrecto! Intente nuevamente...")
        datagram[i] = input(f"Ingrese {i}: ")
        s.send(bytes(f"{i}|{datagram[i]}", "utf-8"))
        code = str(s.recv(128), "utf-8")

    print(f"{i} correcto!")

s.send(b"exit")

s.close()