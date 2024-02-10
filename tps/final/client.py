
  
import argparse
import socket
import time
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip", help="ip", type=str)
parser.add_argument("-p", "--puerto", help="puerto", type=int)
parser.add_argument("-r", "--rol", help="Indica que el tipo de usuario", type=str)

argumento = parser.parse_args()

# Crear el socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conectar al servidor
    sock.connect((argumento.ip, argumento.puerto))
    if argumento.rol:
        msg_rol = argumento.rol.lower()
        sock.sendall(msg_rol.encode())
    
    while True:
        entrada_usuario = input("Ingrese un mensaje: ")
        sock.sendall(entrada_usuario.encode())

        data = sock.recv(1024)
        print("Respuesta del servidor:", data.decode())
except Exception as e:
    print("Error:", e)
finally:
    sock.close()